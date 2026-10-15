import os
import re
import datetime as dt
import boto3

ecr = boto3.client("ecr")
ecs = boto3.client("ecs")
cw = boto3.client("cloudwatch")
sns = boto3.client("sns")

TOPIC_ARN = os.environ["TOPIC_ARN"]
IMAGE_AGE_DAYS = int(os.environ.get("IMAGE_AGE_DAYS", "30"))
KEEP_LATEST_IMAGES = int(os.environ.get("KEEP_LATEST_IMAGES", "10"))
KEEP_TASKDEF_REVISIONS = int(os.environ.get("KEEP_TASKDEF_REVISIONS", "5"))
IDLE_CPU_PERCENT = float(os.environ.get("IDLE_CPU_PERCENT", "5"))
IDLE_DAYS = int(os.environ.get("IDLE_DAYS", "7"))
ECR_GB_MONTH = float(os.environ.get("ECR_GB_MONTH", "0.10"))
VCPU_HOUR = float(os.environ.get("VCPU_HOUR", "0.04048"))
GB_HOUR = float(os.environ.get("GB_HOUR", "0.004445"))

IMAGE_RE = re.compile(
    r"^[^/]+/(?P<repo>[^:@]+)(?::(?P<tag>[^@]+))?(?:@(?P<digest>sha256:[a-f0-9]+))?$"
)


def parse_image(image):
    if ".dkr.ecr." not in image:
        return None
    m = IMAGE_RE.match(image)
    return m.groupdict() if m else None


class Usage:
    """Remembers which ECR images are still referenced by something."""

    def __init__(self):
        self.digests = {}
        self.tags = {}

    def add(self, image, digest=None):
        p = parse_image(image)
        if not p:
            return
        d = digest or p["digest"]
        if d:
            self.digests.setdefault(p["repo"], set()).add(d)
        if p["tag"]:
            self.tags.setdefault(p["repo"], set()).add(p["tag"])

    def used(self, repo, digest, tags):
        return digest in self.digests.get(repo, set()) or any(
            t in self.tags.get(repo, set()) for t in tags
        )


def ignore_ecr(tags):
    return any(t["Key"] == "guardian:ignore" and t["Value"].lower() == "true" for t in tags)


def ignore_ecs(tags):
    return any(t["key"] == "guardian:ignore" and t["value"].lower() == "true" for t in tags)


def list_clusters():
    arns = []
    for p in ecs.get_paginator("list_clusters").paginate():
        arns += p["clusterArns"]
    return arns


def all_services(clusters):
    out = []
    for cluster in clusters:
        arns = []
        for p in ecs.get_paginator("list_services").paginate(cluster=cluster):
            arns += p["serviceArns"]
        for i in range(0, len(arns), 10):
            resp = ecs.describe_services(
                cluster=cluster, services=arns[i:i + 10], include=["TAGS"]
            )
            out += resp["services"]
    return out


def collect_running(clusters, usage, used_taskdefs):
    for cluster in clusters:
        arns = []
        for p in ecs.get_paginator("list_tasks").paginate(cluster=cluster):
            arns += p["taskArns"]
        for i in range(0, len(arns), 100):
            for t in ecs.describe_tasks(cluster=cluster, tasks=arns[i:i + 100])["tasks"]:
                used_taskdefs.add(t["taskDefinitionArn"])
                for c in t["containers"]:
                    usage.add(c.get("image", ""), c.get("imageDigest"))


def scan_taskdefs(used_taskdefs, usage):
    families = {}
    for p in ecs.get_paginator("list_task_definitions").paginate(status="ACTIVE", sort="DESC"):
        for arn in p["taskDefinitionArns"]:
            family = arn.split("/")[-1].rsplit(":", 1)[0]
            families.setdefault(family, []).append(arn)
    stale = []
    for arns in families.values():
        for idx, arn in enumerate(arns):  # newest first
            if idx < KEEP_TASKDEF_REVISIONS or arn in used_taskdefs:
                td = ecs.describe_task_definition(taskDefinition=arn)["taskDefinition"]
                for c in td["containerDefinitions"]:
                    usage.add(c["image"])
            else:
                stale.append(arn)
    return stale


def scan_images(usage, now):
    unused = []
    for p in ecr.get_paginator("describe_repositories").paginate():
        for repo in p["repositories"]:
            name = repo["repositoryName"]
            tags = ecr.list_tags_for_resource(resourceArn=repo["repositoryArn"])["tags"]
            if ignore_ecr(tags):
                continue
            images = []
            for ip in ecr.get_paginator("describe_images").paginate(repositoryName=name):
                images += ip["imageDetails"]
            images.sort(key=lambda i: i["imagePushedAt"], reverse=True)
            for img in images[KEEP_LATEST_IMAGES:]:
                age = (now - img["imagePushedAt"]).days
                itags = img.get("imageTags", [])
                if age >= IMAGE_AGE_DAYS and not usage.used(name, img["imageDigest"], itags):
                    unused.append({
                        "repo": name,
                        "digest": img["imageDigest"],
                        "tags": itags,
                        "age": age,
                        "size": img["imageSizeInBytes"],
                    })
    return unused


def find_idle(services, now):
    idle = []
    for s in services:
        if s.get("status") != "ACTIVE" or s["desiredCount"] == 0:
            continue
        if ignore_ecs(s.get("tags", [])):
            continue
        cluster = s["clusterArn"].split("/")[-1]
        stats = cw.get_metric_statistics(
            Namespace="AWS/ECS",
            MetricName="CPUUtilization",
            Dimensions=[
                {"Name": "ClusterName", "Value": cluster},
                {"Name": "ServiceName", "Value": s["serviceName"]},
            ],
            StartTime=now - dt.timedelta(days=IDLE_DAYS),
            EndTime=now,
            Period=3600,
            Statistics=["Maximum"],
        )
        points = [d["Maximum"] for d in stats["Datapoints"]]
        if not points or max(points) >= IDLE_CPU_PERCENT:
            continue
        td = ecs.describe_task_definition(taskDefinition=s["taskDefinition"])["taskDefinition"]
        monthly = 0.0
        if "FARGATE" in td.get("requiresCompatibilities", []) and td.get("cpu") and td.get("memory"):
            per_hour = int(td["cpu"]) / 1024 * VCPU_HOUR + int(td["memory"]) / 1024 * GB_HOUR
            monthly = per_hour * s["desiredCount"] * 730
        idle.append({
            "cluster": cluster,
            "service": s["serviceName"],
            "tasks": s["desiredCount"],
            "max_cpu": max(points),
            "monthly": monthly,
        })
    return idle


def cleanup(unused, stale):
    by_repo = {}
    for u in unused:
        by_repo.setdefault(u["repo"], []).append({"imageDigest": u["digest"]})
    for repo, ids in by_repo.items():
        for i in range(0, len(ids), 100):
            ecr.batch_delete_image(repositoryName=repo, imageIds=ids[i:i + 100])
    for arn in stale:
        ecs.deregister_task_definition(taskDefinition=arn)


def lambda_handler(event, context):
    mode = (event or {}).get("mode", "report")
    now = dt.datetime.now(dt.timezone.utc)

    usage = Usage()
    clusters = list_clusters()
    services = all_services(clusters)
    used_taskdefs = {s["taskDefinition"] for s in services}
    collect_running(clusters, usage, used_taskdefs)

    stale = scan_taskdefs(used_taskdefs, usage)
    unused = scan_images(usage, now)
    idle = find_idle(services, now)

    if mode == "cleanup":
        cleanup(unused, stale)

    verb = "DELETED" if mode == "cleanup" else "FOUND (dry run, nothing deleted)"
    gb = sum(u["size"] for u in unused) / 1024 ** 3
    ecr_saving = gb * ECR_GB_MONTH
    idle_cost = sum(i["monthly"] for i in idle)
    idle_saving = idle_cost * (1 - 50 / 168)  # running 10h x 5 days instead of 24x7

    lines = [
        f"ECS Guardian report ({mode} mode)",
        "",
        f"1) Unused ECR images {verb}: {len(unused)}  ({gb:.2f} GB, about ${ecr_saving:.2f}/month)",
    ]
    for u in unused:
        lines.append(f"   - {u['repo']} {','.join(u['tags']) or '<untagged>'} ({u['age']} days old)")

    lines += ["", f"2) Stale task definition revisions {verb}: {len(stale)}"]
    for arn in stale:
        lines.append(f"   - {arn.split('/')[-1]}")

    lines += [
        "",
        f"3) Idle ECS services (max CPU under {IDLE_CPU_PERCENT}% for {IDLE_DAYS} days): {len(idle)}",
    ]
    for i in idle:
        lines.append(
            f"   - {i['cluster']}/{i['service']}: {i['tasks']} task(s), max CPU {i['max_cpu']:.1f}%, "
            f"costs about ${i['monthly']:.2f}/month"
        )
    lines += [
        "",
        f"Possible savings: ECR about ${ecr_saving:.2f}/month, "
        f"idle services up to about ${idle_saving:.2f}/month if stopped nights and weekends.",
        "Idle services are never touched automatically. Review them yourself.",
    ]

    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject=f"ECS Guardian: {len(unused)} images, {len(stale)} task defs, {len(idle)} idle services",
        Message="\n".join(lines),
    )
    return {"mode": mode, "unused_images": len(unused), "stale_taskdefs": len(stale), "idle_services": len(idle)}

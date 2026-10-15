# 🧩 Lambda Function

This folder contains the Python source code for the ECS Guardian AWS Lambda function.

## 📄 File Overview

### `container_guardian.py`

The main Lambda function that scans AWS resources, identifies potential waste, estimates cost savings, and sends reports through Amazon SNS.

## ⚙️ How It Works

1. **🔍 Scan ECS Resources** — Discovers ECS clusters, services, running tasks, and task definition revisions.
2. **📦 Inspect ECR Images** — Identifies older container images that are not referenced by running tasks or retained task definitions.
3. **📊 Analyze CPU Utilization** — Uses Amazon CloudWatch metrics to identify potentially idle ECS services.
4. **💰 Estimate Savings** — Calculates approximate ECR storage costs and potential savings from reducing idle-service runtime.
5. **📧 Send Reports** — Publishes findings to the configured Amazon SNS topic.
6. **🧹 Perform Cleanup** — In cleanup mode, deletes eligible ECR images and deregisters eligible ECS task definition revisions.

## 🔄 Execution Modes

| Mode | Description |
|---|---|
| `report` | Scans resources, reports findings, and makes no cleanup changes. This is the default mode. |
| `cleanup` | Performs cleanup of the identified ECR images and ECS task definition revisions. |

Idle ECS services are reported for manual review and are never automatically stopped or deleted.

## 🔑 Required Configuration

The Lambda function reads its configuration from environment variables:

- `TOPIC_ARN` — ARN of the SNS topic used for notifications.
- `IMAGE_AGE_DAYS` — Minimum age for considering ECR images for cleanup.
- `KEEP_LATEST_IMAGES` — Number of newest images to retain in each repository.
- `KEEP_TASKDEF_REVISIONS` — Number of newest task definition revisions to retain.
- `IDLE_CPU_PERCENT` — CPU utilization threshold for identifying potentially idle services.
- `IDLE_DAYS` — Number of days used for idle-service analysis.
- `ECR_GB_MONTH` — Estimated monthly ECR storage cost per GB.
- `VCPU_HOUR` — Estimated Fargate vCPU cost per hour.
- `GB_HOUR` — Estimated Fargate memory cost per GB-hour.

## 🛡️ Safety Notes

- Run `report` mode first and review the findings before using `cleanup` mode.
- Cleanup operations are destructive and should be tested in a dedicated environment.
- The `guardian:ignore=true` tag can exclude supported ECR repositories and ECS services from scanning.
- Cost estimates are approximate and may differ from actual AWS charges.
- Review the implementation and IAM permissions before deploying the function in a production environment.


# 🔐 Security and Safety

ECS Guardian can delete Amazon ECR images and deregister ECS task definition revisions. Its permissions and cleanup workflow are designed to limit unnecessary access and keep destructive actions under human control.

## 🔑 IAM Security and Least Privilege

### How the IAM Policies Are Structured

- **Read access and controlled cleanup:** The Lambda role uses read permissions to inspect ECR, ECS, and CloudWatch resources. The `ecr:BatchDeleteImage` and `ecs:DeregisterTaskDefinition` permissions enable cleanup operations.
- **Restricted notifications:** The `sns:Publish` permission should be scoped to the ARN of the `ecs-guardian-reports` topic.
- **No workload management:** The Lambda role does not need permissions to stop ECS tasks, update services, or modify clusters. Idle services are reported for manual review.
- **Separate IAM roles:** `ContainerGuardianRole` is used by the Lambda function, while `ecsTaskExecutionRole` is used by ECS tasks to pull images and send container logs.
- **Least-privilege access:** Grant only the permissions required by the application, and restrict resource access wherever supported.

## 🛡️ Safety Guardrails

ECS Guardian uses multiple checks to reduce the risk of removing resources that are still needed.

### 1. Report Before Cleanup

The default mode is `report`, which identifies potential cleanup candidates without deleting resources.

Cleanup is triggered explicitly using the event:

`{"mode": "cleanup"}`

The function recalculates its findings when cleanup is invoked rather than relying on an earlier report. Always review the latest report before proceeding.

### 2. Keep the Newest Resources

Two environment variables control resource retention:

- `KEEP_LATEST_IMAGES` — Sets the number of newest ECR images to retain in each repository.
- `KEEP_TASKDEF_REVISIONS` — Sets the number of newest task definition revisions to retain in each family.

### 3. Apply an Image Age Threshold

The `IMAGE_AGE_DAYS` variable defines the minimum age an image must reach before it can be considered for cleanup.

This helps avoid removing recently pushed images.

### 4. Protect Resources in Use

ECS Guardian is designed to identify images referenced by:

- Running ECS tasks.
- Task definitions used by ECS services.
- Task definition revisions selected for retention.

In the demo, image `v2` is used by the running service and retained task definition revisions, while `v4` is protected by the newest-image retention rule.

### 5. Exclude Resources with Tags

Use the tag `guardian:ignore=true` on supported ECR repositories or ECS services to exclude them from scanning.

Apply this tag to resources that should be excluded from the tool's analysis.

### 6. Never Automatically Stop Idle Services

Services with consistently low CPU utilization are included in the SNS report with estimated monthly costs.

ECS Guardian does not automatically stop, scale, or delete these services. A person must review the findings and decide whether action is appropriate.

## ⚠️ Operational Security Recommendations

- Test the function in a dedicated AWS environment before using it on important workloads.
- Start with report mode and inspect the findings before invoking cleanup mode.
- Review the Lambda execution policy whenever the code or its responsibilities change.
- Keep `sns:Publish` restricted to the intended SNS topic.
- Avoid using shared IAM roles for project-specific permissions.
- Verify cleanup candidates and resource dependencies before destructive operations.
- Treat cost-saving figures as estimates, not guaranteed savings.

## 📝 Important Limitation

These guardrails describe the intended safety behavior of ECS Guardian. They do not replace code review, IAM validation, or testing. Resource usage can change between scanning and deletion, so cleanup logic should be validated for race conditions and should recheck resource dependencies before destructive actions.


# 🧹 Cleanup Guide

This guide explains how to remove the AWS resources created for ECS Guardian after testing. Cleaning up these resources helps prevent unnecessary AWS charges, especially from running Amazon ECS Fargate tasks.

## ⚠️ Before You Begin

- Review the resources you created specifically for this project.
- Ensure the `ecs-guardian-weekly` schedule is disabled or deleted to prevent further Lambda invocations.
- Confirm that no other applications depend on the IAM roles, ECR repository, or SNS topic.
- Save any logs or reports you want to keep before deleting them.
- Perform these steps in the same AWS account and Region used during deployment.

**Demo Region:** `ap-south-1` (Mumbai). If you used another Region, select that Region instead.

## 🗑️ Cleanup Workflow

Delete resources in the following order to avoid dependencies and unnecessary charges.

### 1. Delete the EventBridge Scheduler

1. Open **Amazon EventBridge → Scheduler → Schedules**.
2. Find `ecs-guardian-weekly`.
3. Delete the schedule.

This prevents future scheduled invocations of the Lambda function.

### 2. Delete the Lambda Function

1. Open **AWS Lambda → Functions**.
2. Select `container-guardian`.
3. Delete the function and confirm.

### 3. Delete the CloudWatch Log Group

1. Open **CloudWatch → Logs → Log groups**.
2. Find `/aws/lambda/container-guardian`.
3. Delete the log group if you no longer need its logs.

Save any logs required for troubleshooting or documentation before deleting them.

### 4. Delete the ECS Service

1. Open **Amazon ECS → Clusters**.
2. Select `guardian-demo-cluster`.
3. Open the `guardian-demo-svc` service.
4. Delete the service. If prompted, use force deletion only if necessary.
5. Verify that the running Fargate task has stopped.

Deleting the service first is important because it manages the running task.

### 5. Delete the ECS Cluster

1. Return to the `guardian-demo-cluster` page.
2. Delete the cluster after confirming that its services and tasks have been removed.

### 6. Delete the ECR Repository

1. Open **Amazon ECR → Private registry → Repositories**.
2. Select `guardian-demo-app`.
3. Delete the repository and confirm.

This removes the remaining demo container images stored in the repository.

### 7. Delete the SNS Topic

1. Open **Amazon SNS → Topics**.
2. Select `ecs-guardian-reports`.
3. Delete the topic.

The topic's subscriptions are removed with it. Do this only after you have finished testing notifications.

### 8. Remove IAM Roles

Remove the project-specific IAM roles only after confirming they are no longer in use.

- **`ContainerGuardianRole`** — Delete the Lambda execution role and its attached or inline permissions policies.
- **EventBridge Scheduler execution role** — Delete the schedule's execution role if it was created specifically for this project and is no longer used.
- **`ecsTaskExecutionRole`** — Delete the ECS task execution role only if no other ECS tasks or services depend on it.

If a role is shared by other workloads, keep it.

## 💰 Cost Considerations

The most important resource to stop is the running Fargate workload. A running task can continue to incur compute charges even when it receives no traffic.

Other resources, such as ECR image storage, CloudWatch log storage, and related services, may also incur charges depending on usage and pricing.

## 🛡️ Important Notes

- These instructions are intended for the ECS Guardian demo environment, not shared or production infrastructure.
- Deleting resources is permanent or may require recreation. Review each resource before confirming deletion.
- Removing IAM roles can affect other workloads if those roles are shared.
- Check the AWS Billing and Cost Management console after cleanup to review any remaining charges.


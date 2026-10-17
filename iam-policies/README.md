# 🔐 IAM Policies

This folder contains the IAM JSON policies and their corresponding Markdown documentation used to configure permissions and trust relationships for ECS Guardian.

## 📂 Folder Contents

| File | Description |
|---|---|
| `ecs-task-trust-policy.json` | Defines the trust relationship that allows Amazon ECS Tasks to assume the ECS task execution role. |
| `ecs-task-trust-policy.md` | Explains the ECS task trust policy and its purpose in simple terms. |
| `lambda-execution-policy.json` | Defines the permissions required by the Lambda function to scan AWS resources, write logs, publish reports, and perform cleanup operations. |
| `lambda-execution-policy.md` | Explains the Lambda execution permissions and how they are used by ECS Guardian. |

## 🧩 Policy Overview

### 1. ECS Task Trust Policy

The trust policy allows the Amazon ECS Tasks service (`ecs-tasks.amazonaws.com`) to assume the `ecsTaskExecutionRole`.

This role is used by ECS tasks to access required AWS services, such as Amazon ECR for pulling container images and CloudWatch Logs for sending container logs, when the corresponding permissions are attached.

### 2. Lambda Execution Policy

The Lambda execution policy is attached to `ContainerGuardianRole`. It allows the `container-guardian` Lambda function to:

- **Amazon ECR:** Inspect repositories and images, check tags, and delete eligible images during cleanup.
- **Amazon ECS:** Inspect clusters, services, running tasks, and task definition revisions, and deregister eligible revisions during cleanup.
- **Amazon CloudWatch:** Retrieve CPU utilization metrics to identify potentially idle ECS services.
- **CloudWatch Logs:** Record Lambda execution logs.
- **Amazon SNS:** Publish reports to the configured SNS topic.

## ⚙️ Configuration

Before applying the policies:

1. Replace `<YOUR-SNS-TOPIC-ARN>` in `lambda-execution-policy.json` with the actual ARN of your SNS topic.
2. Verify the AWS account ID, Region, role names, and resource ARNs.
3. Attach each policy to the appropriate IAM role or configure the trust relationship as described in its documentation.
4. Review permissions before enabling cleanup operations.

## 🛡️ Security Considerations

- Trust policies specify **who can assume a role**; permissions policies specify **what the role can do**.
- The Lambda execution policy includes image deletion and task definition deregistration permissions. Review report-mode findings before manually invoking cleanup mode.
- Some permissions use `"Resource": "*"`. Restrict resource access where supported and appropriate.
- Keep SNS publishing access limited to the intended topic.
- Test the policies in a dedicated environment before using them in production.


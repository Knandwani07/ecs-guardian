# 🔐 IAM Policy

This folder contains the IAM permissions required by ECS Guardian to scan AWS resources, identify cleanup candidates, write logs, and send reports through Amazon SNS.

## 📄 Lambda Execution Policy

The policy grants the `ContainerGuardianRole` permission to access the AWS services required by ECS Guardian.

### 🧩 Permissions Explained

| AWS Service | Permissions | Purpose |
|---|---|---|
| Amazon CloudWatch Logs | `CreateLogGroup`, `CreateLogStream`, `PutLogEvents` | Creates log groups and streams and records Lambda execution logs. |
| Amazon ECR | `DescribeRepositories`, `DescribeImages`, `ListTagsForResource`, `BatchDeleteImage` | Inspects repositories and images, checks resource tags, and deletes eligible images during cleanup. |
| Amazon ECS | `ListClusters`, `ListServices`, `DescribeServices`, `ListTasks`, `DescribeTasks`, `ListTaskDefinitions`, `DescribeTaskDefinition`, `ListTagsForResource`, `DeregisterTaskDefinition` | Inspects clusters, services, running tasks, and task definition revisions, and deregisters eligible revisions during cleanup. |
| Amazon CloudWatch | `GetMetricStatistics` | Retrieves CPU utilization metrics to identify potentially idle ECS services. |
| Amazon SNS | `Publish` | Sends ECS Guardian reports to the configured SNS topic. |

## ⚙️ Configuration

Before attaching the policy, replace the placeholder below with the ARN of your SNS topic:

`<YOUR-SNS-TOPIC-ARN>`

For this project, the topic is named `ecs-guardian-reports`.

Example ARN format:

`arn:aws:sns:ap-south-1:123456789012:ecs-guardian-reports`

Replace the example account ID with your actual AWS account ID.

## 🚀 How to Attach the Policy

1. Open the **AWS Management Console** and navigate to **IAM**.
2. Select **Roles** and open `ContainerGuardianRole`.
3. Choose **Add permissions** and then **Create inline policy**, or update your existing policy.
4. Open the JSON editor.
5. Paste the policy JSON after replacing the SNS topic ARN placeholder.
6. Review and save the policy.

## 🛡️ Security Notes

- Attach this policy to the Lambda execution role, not the ECS task execution role.
- The policy includes deletion permissions for ECR images and ECS task definition revisions. These actions should only be used after reviewing cleanup findings.
- The policy uses `"Resource": "*"` for several actions. Where supported, restrict access to the specific resources ECS Guardian needs.
- Keep the SNS `Publish` permission limited to the intended topic.
- This policy does not itself control whether the Lambda runs in report or cleanup mode. That behavior depends on the application code.
- Validate the permissions in a test environment before using ECS Guardian against production resources.

## 📝 Important

This is the **Lambda execution policy**. The Lambda function also needs a trusted execution role that allows the AWS Lambda service to assume `ContainerGuardianRole`.

The role's trust policy and the permissions in this document serve different purposes: the trust policy allows Lambda to assume the role, while this permissions policy controls what the function can do.

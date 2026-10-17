# 🔐 Lambda Execution Policy

## 📄 Overview

This document explains the IAM permissions required by the ECS Guardian Lambda function to scan AWS resources, identify potential cleanup candidates, write execution logs, and send reports through Amazon SNS.

The policy is attached to the `ContainerGuardianRole` IAM role.

## ⚙️ Permissions Explained

| AWS Service | Actions | Purpose |
|---|---|---|
| Amazon CloudWatch Logs | `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents` | Creates log groups and streams and records Lambda execution logs. |
| Amazon ECR | `ecr:DescribeRepositories`, `ecr:DescribeImages`, `ecr:ListTagsForResource` | Lists repositories, inspects container images, and checks repository tags. |
| Amazon ECR | `ecr:BatchDeleteImage` | Deletes eligible container images when cleanup mode is invoked. |
| Amazon ECS | `ecs:ListClusters`, `ecs:ListServices`, `ecs:DescribeServices`, `ecs:ListTasks`, `ecs:DescribeTasks` | Discovers clusters, inspects services, and checks running tasks. |
| Amazon ECS | `ecs:ListTaskDefinitions`, `ecs:DescribeTaskDefinition`, `ecs:ListTagsForResource` | Inspects task definition revisions and resource tags. |
| Amazon ECS | `ecs:DeregisterTaskDefinition` | Deregisters eligible task definition revisions during cleanup. |
| Amazon CloudWatch | `cloudwatch:GetMetricStatistics` | Retrieves CPU utilization metrics to identify potentially idle ECS services. |
| Amazon SNS | `sns:Publish` | Sends reports to the configured SNS topic. |

## 🎯 How It Works

1. **Scan Resources** — Reads ECR repositories, images, ECS clusters, services, tasks, and task definition revisions.
2. **Analyze Metrics** — Retrieves CloudWatch CPU statistics to identify potentially idle services.
3. **Record Logs** — Writes execution details to CloudWatch Logs.
4. **Send Reports** — Publishes findings to the configured SNS topic.
5. **Perform Cleanup** — Uses the ECR deletion and ECS deregistration permissions when cleanup mode is invoked.

## 🛠️ Configuration

Before attaching the policy, replace:

`<YOUR-SNS-TOPIC-ARN>`

with the actual ARN of your SNS topic, such as the `ecs-guardian-reports` topic created for this project.

An SNS topic ARN follows this format:

`arn:aws:sns:ap-south-1:123456789012:ecs-guardian-reports`

Replace the example account ID with your actual AWS account ID.

## 🚀 How to Attach the Policy

1. Open **AWS Console → IAM → Roles**.
2. Select `ContainerGuardianRole`.
3. Choose **Add permissions** or edit the existing inline policy.
4. Open the JSON policy editor.
5. Add the permissions policy after replacing the SNS ARN placeholder.
6. Review and save the policy.

## 🛡️ Security Notes

- This is a **permissions policy**, not a trust policy. The Lambda execution role also needs a trust relationship allowing `lambda.amazonaws.com` to assume it.
- The policy grants deletion and deregistration permissions. Review report-mode findings before invoking cleanup mode.
- `Resource: "*"` grants broad access for the listed actions. Restrict resource access where AWS supports it and your application permits it.
- Keep `sns:Publish` limited to the intended SNS topic.
- Test the policy in a dedicated environment before using it against production resources.


# 🔐 ECS Task Trust Policy

## 📄 Overview

This document explains the IAM trust policy that allows Amazon ECS tasks to assume an IAM role.

The policy uses the AWS Security Token Service (AWS STS) action `sts:AssumeRole` to allow the Amazon ECS Tasks service to assume the role.

## ⚙️ Policy Explanation

| Field | Purpose |
|---|---|
| `Version` | Specifies the policy language version, `2008-10-17`. |
| `Effect` | `Allow` means the specified action is permitted. |
| `Principal` | Identifies `ecs-tasks.amazonaws.com` as the AWS service allowed to assume the role. |
| `Action` | `sts:AssumeRole` allows the trusted service to assume the IAM role. |
| `Sid` | An optional statement identifier; it is empty in this policy. |

## 🎯 Why Is This Required?

ECS Guardian's demo uses an ECS task execution role named `ecsTaskExecutionRole`.

The trust policy allows the Amazon ECS Tasks service to assume that role. The permissions attached to the role determine what the role can do, such as pulling container images from Amazon ECR and sending logs to CloudWatch Logs.

**Important:** This trust policy does not grant ECR or CloudWatch permissions by itself. Those permissions must be attached separately through an IAM permissions policy.

## 🛠️ Where to Configure It

1. Open the AWS Management Console.
2. Navigate to **IAM → Roles**.
3. Create or open `ecsTaskExecutionRole`.
4. In the trust relationship configuration, ensure the trusted service is `ecs-tasks.amazonaws.com`.
5. Attach the appropriate permissions policy to the role.

## 🛡️ Security Note

Use this trust policy for the ECS task execution role when appropriate. The Lambda execution role (`ContainerGuardianRole`) has a different purpose and requires its own trust policy that allows the AWS Lambda service to assume it.


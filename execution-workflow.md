# 🛠️ Execution Guide

This guide outlines the execution workflow of ECS Guardian, from provisioning AWS resources to running reports, performing manual cleanup, and scheduling weekly reports.

## 🔄 Execution Diagram

<img width="811" height="677" alt="Screenshot 2026-10-11 220436" src="https://github.com/user-attachments/assets/3f52bc00-50dd-4166-9c6e-5ad9765c6b3b" />

## 📋 Execution Workflow

### Step I: Configure SNS Notifications
Create the `ecs-guardian-reports` SNS topic, subscribe your email address, and confirm the subscription to receive Guardian reports.

### Step II: Provision Demo Resources
Create the `ecsTaskExecutionRole` IAM role and the `guardian-demo-app` ECR repository. Push four container images (`v1`–`v4`), register six task definition revisions, and create the `guardian-demo-cluster` cluster with the `guardian-demo-svc` service running revision 6.

### Step III: Configure Lambda Permissions
Create the `ContainerGuardianRole` IAM role and attach the required permissions for ECR, ECS, CloudWatch, CloudWatch Logs, and publishing reports through SNS.

### Step IV: Deploy the Lambda Function
Create the `container-guardian` Lambda function using Python 3.12. Deploy the Guardian implementation and configure the required environment variables and execution settings.

### Step V: Run Report Mode
Invoke the Lambda function with report mode enabled. Review the email report for unused ECR images, stale task definition revisions, potentially idle ECS services, and estimated savings. No resources should be deleted in this mode.

### Step VI: Run Cleanup Mode
After reviewing the findings, manually invoke cleanup mode if cleanup is required. Verify the ECR images and ECS task definition revisions afterward. Idle services remain untouched.

### Step VII: Schedule Weekly Reports
Configure the `ecs-guardian-weekly` EventBridge schedule to invoke Lambda every Monday at 9:00 AM IST, using report mode.

### Step VIII: Clean Up Demo Resources
Delete the EventBridge schedule, Lambda function, CloudWatch log group, ECS service and cluster, ECR repository, SNS topic, and associated IAM roles when testing is complete.

## 🛡️ Execution Notes

- Always run report mode before cleanup.
- Keep scheduled executions in report mode.
- Verify findings before performing destructive operations.
- Review estimated savings as approximations, not guaranteed cost reductions.
- Remove demo resources after testing to avoid unnecessary AWS charges.

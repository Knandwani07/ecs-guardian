# ECS Guardian 🛡️

A serverless AWS housekeeping tool that identifies unused Amazon ECR images, stale ECS task definition revisions, and potentially idle ECS services.

## 🎯 Overview

ECS Guardian uses AWS Lambda to scan container resources, identify potential waste, estimate cost savings, and send reports through Amazon SNS.

It supports two modes:

- **Report Mode:** Identifies unused resources without deleting anything.
- **Cleanup Mode:** Deletes eligible unused ECR images and deregisters stale ECS task definition revisions when manually triggered.

Idle ECS services are reported for manual review and are never automatically modified.

## 🏗️ Architecture

**AWS Services Used:**
- AWS Lambda
- Amazon ECR
- Amazon ECS
- Amazon CloudWatch
- Amazon SNS
- Amazon EventBridge Scheduler
- AWS IAM

## ✨ Key Features

- Detects old, unused container images.
- Identifies stale ECS task definition revisions.
- Reports potentially idle ECS services.
- Estimates potential monthly cost savings.
- Supports scheduled weekly reports.
- Includes resource protection through usage checks and ignore tags.

## ⚙️ Configuration

Thresholds are configurable through Lambda environment variables, including:

- `IMAGE_AGE_DAYS`
- `KEEP_LATEST_IMAGES`
- `KEEP_TASKDEF_REVISIONS`
- `IDLE_CPU_PERCENT`
- `IDLE_DAYS`
- `TOPIC_ARN`

## 🚀 Project Status

This project is under development. Setup instructions, architecture diagrams, source code, and testing details will be added and updated.

## 🔐 Safety

Always run report mode and review the findings before triggering cleanup. Test in a non-production AWS environment before using the tool on real workloads.

## 📄 License

License to be added.

---

**Built with AWS services and Python (boto3).**

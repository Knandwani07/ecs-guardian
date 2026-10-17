# 🛠️ Scripts

This folder contains shell scripts used to prepare and configure the AWS resources required for testing.

## 📄 Contents

| File | Description |
|---|---|
| `push-demo-images.sh` | Builds sample Docker images and pushes them to Amazon ECR. |
| `register-task-definitions.sh` | Registers multiple ECS task definition revisions using different container image versions. |
| `script-details.md` | Explains the purpose, execution flow, prerequisites, and usage of each script. |

## 🎯 Purpose

These scripts automate the initial setup of demo resources for testing ECS Guardian. They create sample container images and task definition revisions that help demonstrate how the tool identifies potentially unused resources.

## ⚙️ Prerequisites

- AWS CLI installed and configured.
- Docker installed and running.
- Appropriate AWS IAM permissions.
- The required ECR repository and execution role created before running the relevant scripts.

## ⚠️ Important Notes

- The scripts currently use `ap-south-1` (Mumbai). You can use another AWS Region, provided all required resources are available there and the scripts are configured consistently.
- Review account IDs, resource names, and IAM role ARNs before execution.
- Run the scripts in the intended AWS account to avoid creating resources in the wrong environment.


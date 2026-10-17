# 🛠️ Scripts

This folder contains shell scripts and their documentation for preparing the demo resources used to test ECS Guardian.

## 📄 Folder Contents

| File | Description |
|---|---|
| `push-demo-images.sh` | Builds sample Docker images tagged `v1`, `v2`, `v3`, and `v4`, then pushes them to Amazon ECR. |
| `push-demo-images.md` | Explains the image build and push process, prerequisites, and execution steps. |
| `register-task-definitions.sh` | Registers six revisions of the `guardian-demo-task` ECS task definition family using the demo images. |
| `register-task-definitions.md` | Explains task definition registration, the image sequence, prerequisites, and required IAM permissions. |

## 🎯 Purpose

These scripts automate two preparation tasks:

1. **Build and Push Images** — Creates sample container images and uploads them to Amazon ECR.
2. **Register Task Definitions** — Creates multiple ECS task definition revisions to help demonstrate how ECS Guardian identifies potentially unused resources.

The Markdown files provide instructions and explain the purpose of each script without duplicating the shell commands.

## ⚙️ Prerequisites

Before running the scripts, ensure you have:

- AWS CLI installed and configured.
- Docker installed and running.
- Valid AWS credentials and the required IAM permissions.
- The `guardian-demo-app` ECR repository created in the selected Region.
- The `ecsTaskExecutionRole` IAM role configured.
- The required ECR images available before registering task definitions.

## 🌏 AWS Region

The scripts use `ap-south-1` (Mumbai) by default. You can choose another AWS Region, provided the required resources exist there and the scripts are configured consistently.

## ⚠️ Important Notes

- Verify your AWS account ID, Region, repository URI, and IAM role ARN before execution.
- The image-push script creates or overwrites local Docker build files in its working directory.
- Registering task definitions creates additional revisions in your AWS account.
- These scripts prepare demo resources; they do not deploy the ECS Guardian Lambda function.
- Review the individual Markdown guides before running either script.


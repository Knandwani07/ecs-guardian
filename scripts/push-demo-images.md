# 🐳 Docker Image Build and Push

This folder contains the script used to build sample Docker images and push them to Amazon Elastic Container Registry (Amazon ECR) for testing.

## 📄 File Overview

### `push-demo-images.sh`

Automates the process of building and uploading four demo images (`v1`, `v2`, `v3`, and `v4`) to the `guardian-demo-app` ECR repository.

## ⚙️ How It Works

1. **Configure AWS Region** — Sets the AWS Region to `ap-south-1` (Mumbai).
2. **Retrieve AWS Account ID** — Uses AWS STS to identify the currently configured AWS account.
3. **Construct Repository URI** — Builds the ECR repository address for `guardian-demo-app`.
4. **Authenticate Docker** — Retrieves an Amazon ECR login password and signs Docker in to the registry.
5. **Build Docker Images** — Creates four small NGINX-based images, each containing a different version label.
6. **Push Images to ECR** — Uploads each image using its version tag.
7. **Add a Short Delay** — Waits briefly between image pushes.

## 📦 Why These Images Are Needed

The images provide test data for ECS Guardian. Different versions help demonstrate how the tool identifies potentially unused images while protecting images referenced by running tasks or retained task definitions.

## ✅ Prerequisites

- AWS CLI installed and configured.
- Docker installed and running.
- Permission to authenticate with and push images to Amazon ECR.
- The `guardian-demo-app` ECR repository created in the selected AWS Region.

## ▶️ Usage

Run the script from a terminal with the required AWS credentials configured. Ensure the repository exists before running it.

## 📝 Important Notes

- The script targets the `ap-south-1` Region.
- It creates a local `guardian-demo` directory and writes a Dockerfile into it.
- Re-running the script pushes images with the same tags, which can update those tags in ECR.
- Review the AWS account and Region before running the script to avoid pushing images to the wrong repository.

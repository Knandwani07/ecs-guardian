# 🏗️ Architecture Overview

This project implements a **serverless AWS housekeeping architecture** using AWS Lambda, Amazon ECR, Amazon ECS, Amazon CloudWatch, Amazon SNS, and Amazon EventBridge Scheduler.

ECS Guardian scans container images, ECS task definition revisions, and services to identify potential resource waste and estimate cost savings. It sends reports through Amazon SNS and supports two operating modes: **Report Mode**, which identifies resources without deleting anything, and **Cleanup Mode**, which removes eligible unused images and deregisters stale task definition revisions when manually triggered.

The project is demonstrated in the **Mumbai (`ap-south-1`) AWS Region**.

## 🖼️ Architecture Diagram

<!-- Add the ECS Guardian architecture diagram here -->

<img width="1672" height="941" alt="AWS_Diagram" src="https://github.com/user-attachments/assets/f0ad9f5a-f4c3-48e1-85dc-078c5a2f311d" />


# 🧩 AWS Components

* **AWS Lambda (`container-guardian`)** — Scans AWS resources, evaluates usage, estimates potential savings, and coordinates reporting or cleanup.
* **Amazon ECR (`guardian-demo-app`)** — Stores container images and identifies images that meet the age and retention criteria for cleanup.
* **Amazon ECS (`guardian-demo-cluster`)** — Hosts the demo service and running tasks used to identify resources still in use.
* **ECS Task Definitions (`guardian-demo-task`)** — Stores task definition revisions and helps identify stale revisions beyond the configured retention limit.
* **Amazon CloudWatch Metrics** — Provides ECS CPU utilization data to identify potentially idle services.
* **Amazon SNS (`ecs-guardian-reports`)** — Delivers findings and estimated savings to the subscribed email address.
* **Amazon EventBridge Scheduler (`ecs-guardian-weekly`)** — Invokes Lambda every Monday at 9:00 AM IST in report mode.
* **Amazon CloudWatch Logs** — Stores Lambda execution logs for troubleshooting.
* **IAM (`ContainerGuardianRole`)** — Grants the Lambda function permissions to inspect resources, publish reports, and perform authorized cleanup actions.
* **IAM (`ecsTaskExecutionRole`)** — Allows Fargate tasks to pull images from ECR and send container logs.
* **Resource Tags (`guardian:ignore=true`)** — Exempt tagged ECR repositories and ECS services from their respective scans.


## 🌏 Region

This project uses the **Mumbai (`ap-south-1`) AWS Region**. Resource names, IAM ARNs, and configuration values may need to be adjusted when deploying in another Region.

## 💰 Cost Considerations

The demo uses a small Fargate task with 0.25 vCPU and 0.5 GB of memory. AWS charges may apply for running resources and service usage.

The reported savings are estimates, not guaranteed reductions. Configure the ECR and Fargate pricing values for the deployment Region, and remove demo resources when testing is complete.

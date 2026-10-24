# ECS Guardian: A Serverless Solution for Container Resource Lifecycle Management 🛡️

**A serverless AWS housekeeping tool to identify unused container images, stale ECS task definition revisions, and potentially idle services with cost reports and human-controlled cleanup.**

ECS Guardian uses AWS Lambda to scan Amazon ECR, Amazon ECS, and Amazon CloudWatch. It identifies potential resource waste and sends findings and estimated savings through Amazon SNS.

The project follows a safety-first approach: reporting is the default, cleanup is triggered manually, and idle ECS services are only reported for human review.

## ✨ Key Features

- **Unused ECR Image Detection** — Identifies images that exceed a configured age threshold, fall outside the newest-N retention rule, and are not considered in use.
- **Stale Task Definition Detection** — Finds older ECS task definition revisions that fall outside the retention limit and are not identified as in use.
- **Idle Service Analysis** — Uses CloudWatch CPU utilization metrics to identify potentially idle ECS services.
- **Cost Estimation** — Estimates ECR storage costs and potential savings from reducing idle-service runtime.
- **Email Notifications** — Sends resource findings and cost estimates through Amazon SNS.
- **Scheduled Reporting** — Supports weekly report-only execution through Amazon EventBridge Scheduler.
- **Safety Controls** — Supports report and cleanup modes, configurable retention thresholds, and the `guardian:ignore=true` exclusion tag.

## 🔄 Execution Modes

| Mode | Behavior |
|---|---|
| `report` | Scans resources and sends findings without performing cleanup. This is the default mode. |
| `cleanup` | Deletes eligible ECR images and deregisters eligible ECS task definition revisions. Invoked manually. |

**Important:** Idle ECS services are never automatically stopped, scaled, or deleted. They are reported for manual review.

## 🧪 Demo Environment

The project includes a demo environment for validating the scanning and cleanup workflow.

| Resource | Demo Configuration |
|---|---|
| AWS Region | `ap-south-1` (Mumbai) |
| Lambda function | `container-guardian` |
| ECR repository | `guardian-demo-app` |
| ECS cluster | `guardian-demo-cluster` |
| ECS service | `guardian-demo-svc` |
| Task definition family | `guardian-demo-task` |
| SNS topic | `ecs-guardian-reports` |
| EventBridge schedule | `ecs-guardian-weekly` |

You can use another AWS Region, provided the resources and configuration are consistent throughout the deployment.

## 📚 Documentation

| Document | Description |
|---|---|
| [Architecture Overview](architecture-overview.md) | Explains the architecture and AWS components. |
| [Execution Workflow](execution-workflow.md) | Describes the overall execution flow and setup sequence. |
| [Security and Safety](security.md) | Documents IAM security principles and safety guardrails. |
| [Best Practices and Lessons Learned](best-practices.md) | Covers recommended operating practices and lessons from testing. |
| [Execution Outcome](execution-outcome.md) | Summarizes the demonstrated cleanup actions and reported findings. |
| [Cleanup Guide](cleanup-guide.md) | Explains how to remove demo resources after testing. |

## 📁 Repository Structure

```text
ecs-guardian/
├── iam-policies/
│   ├── README.md
│   ├── ecs-task-trust-policy.json
│   ├── ecs-task-trust-policy.md
│   ├── lambda-execution-policy.json
│   └── lambda-execution-policy.md
├── scripts/
│   ├── README.md
│   ├── push-demo-images.sh
│   ├── push-demo-images.md
│   ├── register-task-definitions.sh
│   └── register-task-definitions.md
├── src/
│   ├── README.md
│   └── container_guardian.py
├── ecs_guardian_project_documentation.pdf
├── README.md
├── architecture-overview.md
├── best-practices.md
├── cleanup-guide.md
├── execution-outcome.md
├── execution-workflow.md
└── security.md
```

## 📂 Repository Contents

| File / Folder | Description |
|---|---|
| `iam-policies/` | Contains IAM trust and permissions policies in JSON format, along with Markdown explanations. |
| `scripts/` | Contains shell scripts for building and pushing demo Docker images to Amazon ECR and registering ECS task definition revisions. 
| `src/` | Contains the Python source code for the AWS Lambda function and its documentation. |
| `ecs_guardian_project_documentation.pdf/` | Provides the consolidated ECS Guardian project documentation in PDF format.|
| `README.md` | Main project overview, features, architecture summary, and links to supporting documentation. |
| `architecture-overview.md` | Explains the system architecture, AWS services, and their responsibilities. |
| `execution-workflow.md` | Describes the execution workflow and the sequence of steps used to prepare and run the demo. |
| `execution-outcome.md` | Documents the cleanup execution report, including deleted ECR images, deregistered task definition revisions, and idle-service findings. |
| `security.md` | Explains IAM security, least-privilege principles, and safety guardrails. |
| `best-practices.md` | Covers recommended configurations, operational practices, and lessons learned. |
| `cleanup-guide.md` | Provides instructions for removing demo AWS resources after testing. |


## 🚀 Getting Started

Follow the documentation in this order:

1. **Review the architecture** — Understand the AWS services and their relationships.
2. **Review IAM policies** — Configure the required trust relationships and permissions.
3. **Prepare demo resources** — Use the scripts in `scripts/` to push container images and register task definition revisions.
4. **Deploy the Lambda function** — Follow the deployment steps and configure the required environment variables.
5. **Run report mode** — Review the SNS email and verify the findings.
6. **Test cleanup mode** — Only after reviewing the report, manually invoke cleanup and verify the resulting resource state.
7. **Configure scheduled reporting** — Keep the scheduled payload in report mode.
8. **Clean up the demo** — Follow the cleanup guide to remove resources you no longer need.


## 🤝 Let's Connect

- 💼 **LinkedIn:** https://www.linkedin.com/in/khushi-nandwani/
- 💻 **GitHub:** https://github.com/Knandwani07
- ✍️ **Dev Community:** https://dev.to/khushi_nandwani07
- 📝 **Medium:** https://medium.com/@khushinandwanii
- 🌐 **Portfolio:** https://main.d1n4wt6uo5bfx6.amplifyapp.com/

---

⭐ **If you found this project helpful, consider giving it a star!**

Suggestions, improvements, and feedback are welcome. Feel free to open an issue or submit a pull request.


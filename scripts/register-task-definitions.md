## 📄 `register-task-definitions.sh`

This script registers six revisions of the ECS task definition family `guardian-demo-task`. Each revision uses the same NGINX container configuration but references a different image tag.

### ⚙️ How It Works

1. **Set AWS Region** — Uses `ap-south-1` (Mumbai). You can choose another Region if your resources are deployed there.
2. **Get AWS Account ID** — Retrieves the account ID for the currently configured AWS credentials.
3. **Build ECR Image URI** — Constructs the URI for the `guardian-demo-app` repository.
4. **Register Task Definitions** — Creates six revisions using the image sequence `v1`, `v2`, `v3`, `v4`, `v2`, `v2`.
5. **Display Revision Numbers** — Prints each newly registered task definition revision.

### 🎯 Why Six Revisions?

The different revisions provide test data for ECS Guardian to identify older task definition revisions while retaining the newest revisions and protecting definitions referenced by ECS services or running tasks.

### ⚠️ Before Running

- Replace `accountid` in the execution role ARN with your actual AWS account ID.
- Ensure the `ecsTaskExecutionRole` exists and has the required permissions.
- Confirm that the ECR repository and all four image tags exist in the selected Region.
- Ensure your AWS identity has permission to register ECS task definitions and pass the execution role (`iam:PassRole`).


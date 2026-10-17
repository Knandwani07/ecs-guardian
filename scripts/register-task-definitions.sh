# You can choose any AWS Region you prefer. I am using ap-south-1 (Mumbai) for this project.
export AWS_REGION=ap-south-1
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export REPO_URI=$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/guardian-demo-app

for v in v1 v2 v3 v4 v2 v2; do aws ecs register-task-definition --family guardian-demo-task --requires-compatibilities FARGATE --network-mode awsvpc --cpu 256 --memory 512 --execution-role-arn arn:aws:iam::accountid:role/ecsTaskExecutionRole --container-definitions "[{\"name\":\"web\",\"image\":\"$REPO_URI:$v\",\"essential\":true,\"portMappings\":[{\"containerPort\":80}]}]" --region ap-south-1 --query 'taskDefinition.revision' --output text; done

# You can choose any AWS Region you prefer. I am using ap-south-1 (Mumbai) for this project.
export AWS_REGION=ap-south-1
export AWS_DEFAULT_REGION=ap-south-1
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export REPO_URI=$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/guardian-demo-app

aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

mkdir -p guardian-demo && cd guardian-demo

for v in v1 v2 v3 v4; do
    printf 'FROM public.ecr.aws/docker/library/nginx:alpine\nRUN echo %s > /usr/share/nginx/html/version.txt\n' "$v" > Dockerfile
    docker build -t "$REPO_URI:$v" .
    docker push "$REPO_URI:$v"
    sleep 2
done

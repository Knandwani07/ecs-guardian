# ✅ Best Practices and Lessons Learned

This document outlines practical recommendations for running ECS Guardian safely, validating its findings, and managing AWS resource costs.

## 🛡️ Operational Best Practices

- **Start with a dry run.** Run `report` mode first and review the findings carefully before invoking cleanup.
- **Use conservative thresholds in production.** Aggressive test values such as `IMAGE_AGE_DAYS=0` help demonstrate the tool. For production, consider an image age of 30 days, retaining 10 images, and keeping 5 task definition revisions.
- **Tag protected resources early.** Apply `guardian:ignore=true` to supported ECR repositories or ECS services that should be excluded from scanning.
- **Allow time for CloudWatch metrics.** Idle-service detection depends on available metrics. Wait around 10 minutes after starting a service for initial data, and consider `IDLE_DAYS=7` for production to reduce false positives.
- **Use region-appropriate pricing.** Configure `VCPU_HOUR` and `GB_HOUR` using the applicable regional Fargate prices to improve cost estimates.
- **Keep scheduled execution in report mode.** Automate weekly reports, but keep cleanup as a deliberate manual action.
- **Understand image digests and tags.** Multiple tags can reference the same image digest. Deleting an image should be evaluated by digest and remaining references, not just by tag.
- **Clean up test resources promptly.** A running Fargate task can continue to incur charges until its service and workload are stopped.

## 💡 Lessons Learned

ECS Guardian demonstrates that cloud housekeeping requires more than identifying old resources. Resource usage, retention rules, monitoring data, IAM permissions, and human review all matter.

A safe workflow combines automated detection with explicit approval for destructive actions, while cost estimates help prioritize resources for further investigation.


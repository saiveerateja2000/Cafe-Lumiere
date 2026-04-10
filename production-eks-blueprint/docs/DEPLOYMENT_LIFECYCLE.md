# Deployment Lifecycle (Dev -> Staging -> Prod)

1. Developer pushes code.
2. CI runs tests, linting, SAST/SCA, and container image scanning.
3. Docker images built and pushed to ECR with immutable SHA tag.
4. GitOps manifests updated with new image tag.
5. ArgoCD syncs `dev` first.
6. Smoke tests + SLO checks validate deployment.
7. Manual or policy approval promotes to `staging`.
8. Canary or blue/green rollout in `prod`.
9. If error budget burn/high 5xx occurs, rollback by reverting Git commit.

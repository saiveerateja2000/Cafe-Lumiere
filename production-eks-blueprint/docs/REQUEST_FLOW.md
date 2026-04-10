# End-to-End Request Flow

1. User requests `https://app.example.com` in browser.
2. Route53 resolves domain to ALB DNS.
3. AWS WAF evaluates rules and blocks malicious payloads/IPs.
4. ALB terminates TLS using ACM certificate.
5. ALB performs Cognito authentication challenge if session is missing.
6. ALB forwards traffic by path rule:
   - `/` -> `frontend-service`
   - `/api/users` -> `user-service`
   - `/api/orders` -> `order-service`
   - `/health` -> `health-service`
7. Backend services load configuration from ConfigMap and secrets from synced Kubernetes Secret.
8. Backend connects to PostgreSQL StatefulSet service `postgres:5432`.
9. Response flows back through ALB to browser.
10. Metrics/logs/traces are scraped by Prometheus and visualized in Grafana.

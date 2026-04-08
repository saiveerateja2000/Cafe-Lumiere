# Grafana Enterprise: Setup, Governance, and RBAC

## Deployment Foundations
- Run Grafana with persistent storage for provisioning and plugins.
- Use external PostgreSQL/MySQL for Grafana metadata in production.
- Enable HTTPS and enforce secure cookies.

## Authentication and SSO
- Integrate with enterprise IdP (Azure AD/Okta/LDAP/SAML/OIDC).
- Disable local admin usage for routine operations.
- Enforce MFA through IdP policy.

## RBAC Model
- Organizations for strict tenancy boundaries (if required).
- Teams aligned to service ownership.
- Folder permissions for dashboard and alert ownership.
- Data source permissions to enforce least privilege.

## Provisioning as Code
- Use provisioning files/Terraform for data sources, folders, dashboards, alert rules.
- Keep changes in Git and code review.
- Avoid manual production edits except emergency break-glass.

## Enterprise Features to Adopt
- Reporting and scheduled dashboard exports.
- Fine-grained access control and audit logs.
- Advanced data source permissions and query governance.

## Operational Controls
- Backup Grafana DB daily.
- Version pin dashboards and plugins.
- Validate plugin compatibility before upgrades.

## Upgrade Strategy
- Stage environment first.
- Backup metadata DB and provisioning bundles.
- Perform canary upgrade and smoke tests (dashboard load, alert test, SSO login).

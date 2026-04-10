# Terraform Layout

Use reusable modules with environment compositions:

- `modules/`: shared reusable IaC units
- `environments/dev|staging|prod`: stack composition for each environment

Recommended remote state: S3 backend + DynamoDB lock table.

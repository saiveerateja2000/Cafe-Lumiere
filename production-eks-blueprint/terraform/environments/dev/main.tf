terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "../../modules/vpc"
  name   = "cafe-dev"
}

module "eks" {
  source       = "../../modules/eks"
  cluster_name = "cafe-dev"
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids
}

module "ecr" {
  source       = "../../modules/ecr"
  repositories = ["frontend", "user-service", "order-service", "health-service"]
}

module "acm" {
  source      = "../../modules/acm"
  domain_name = "dev.app.example.com"
}

module "route53" {
  source       = "../../modules/route53"
  zone_name    = "example.com"
  record_name  = "dev.app.example.com"
  alb_dns_name = module.eks.alb_dns_name
}

module "cognito" {
  source = "../../modules/cognito"
  name   = "cafe-dev"
}

module "waf" {
  source = "../../modules/waf"
  name   = "cafe-dev"
}

module "iam" {
  source       = "../../modules/iam"
  cluster_name = module.eks.cluster_name
}

module "secrets_manager" {
  source      = "../../modules/secrets-manager"
  secret_name = "cafe/dev/app"
}

module "monitoring" {
  source       = "../../modules/monitoring"
  cluster_name = module.eks.cluster_name
}

module "alb_controller" {
  source       = "../../modules/alb-controller"
  cluster_name = module.eks.cluster_name
}

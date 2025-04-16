module "vpc" {
  source = "./modules/vpc"

  project_name        = "f1-stats-app"
  vpc_cidr           = "10.0.0.0/16"
  public_subnets     = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets    = ["10.0.3.0/24", "10.0.4.0/24"]
  availability_zones = ["ap-south-1a", "ap-south-1b"]
}

module "nat" {
  source = "./modules/nat"

  project_name       = "f1-stats-app"
  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
}

module "security" {
  source = "./modules/security"

  project_name    = "f1-stats-app"
  vpc_id         = module.vpc.vpc_id
  container_port = 8000
}

module "alb" {
  source = "./modules/alb"

  project_name       = "f1-stats-app"
  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  security_group_id = module.security.alb_security_group_id
  health_check_path = "/"
}

module "iam" {
  source       = "./modules/iam"
}

module "ecs" {
  source = "./modules/ecs"

  project_name                = "f1-stats-app"
  aws_region                 = "ap-south-1"
  vpc_id                     = module.vpc.vpc_id
  private_subnet_ids         = module.vpc.private_subnet_ids
  security_group_id          = module.security.ecs_security_group_id
  alb_target_group_arn       = module.alb.target_group_arn
  container_image            = "" // Your Container Image
  container_port             = 8000
  container_cpu              = 256
  container_memory           = 512
  desired_count              = 2
  ecs_task_execution_role_arn = module.iam.ecs_task_execution_role_arn
  ecs_task_role_arn          = module.iam.ecs_task_role_arn
}

module "dynamodb" {
  source = "./modules/dynamodb"

  project_name = "f1-stats-app"
  table_name   = "f1-stats-cache"
  vpc_id       = module.vpc.vpc_id  # Added missing vpc_id for DynamoDB endpoint
}


# Add outputs
output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = module.alb.alb_dns_name
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = module.dynamodb.table_name
}
variable "project_name" {
  type        = string
  description = "Name of the project"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
}

variable "vpc_id" {
  type        = string
  description = "ID of the VPC"
}

variable "private_subnet_ids" {
  type        = list(string)
  description = "List of private subnet IDs"
}

variable "security_group_id" {
  type        = string
  description = "Security group ID for ECS tasks"
}

variable "alb_target_group_arn" {
  type        = string
  description = "ARN of the ALB target group"
}

variable "container_image" {
  type        = string
  description = "Docker image to run in the ECS cluster"
}

variable "container_port" {
  type        = number
  description = "Port exposed by the container"
}

variable "container_cpu" {
  type        = number
  description = "CPU units for the container"
}

variable "container_memory" {
  type        = number
  description = "Memory limit for the container"
}

variable "desired_count" {
  type        = number
  description = "Number of instances of the task to run"
}

variable "ecs_task_execution_role_arn" {
  type        = string
  description = "ARN of the ECS task execution role"
}

variable "ecs_task_role_arn" {
  type        = string
  description = "ARN of the ECS task role"
}
# Add terraform block for version constraints
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  required_version = ">= 1.0"
}

# Add provider configuration
provider "aws" {
  region = "ap-south-1"
}
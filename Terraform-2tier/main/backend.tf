terraform {
  backend "s3" {
    bucket  = "2tier-architecture-bucket"
    key     = "2tier-architecture.tfstate"
    region  = "ap-south-1"
    profile = "default"
  }
}


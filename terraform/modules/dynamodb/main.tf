# Add this at the top of the file
data "aws_region" "current" {}

resource "aws_dynamodb_table" "main" {
  name           = var.table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "endpoint"
  range_key      = "timestamp"

  attribute {
    name = "endpoint"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

  ttl {
    attribute_name = "expiry_time"
    enabled        = true
  }

  tags = {
    Name = "${var.project_name}-dynamodb"
  }
}

resource "aws_vpc_endpoint" "dynamodb" {
  vpc_id       = var.vpc_id
  service_name = "com.amazonaws.${data.aws_region.current.name}.dynamodb"

  tags = {
    Name = "${var.project_name}-dynamodb-endpoint"
  }
}
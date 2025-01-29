
# Two-Tier Architecture on AWS using Terraform

This project demonstrates the deployment of a two-tier architecture on AWS using Terraform. The architecture consists of a highly available web application running on EC2 instances with a MySQL RDS database in the backend, ensuring scalability and reliability.

## Architectural Diagram
## Tech Stack

**Infrastructure as Code (IaC):** Terraform

**Cloud Provider:** AWS

**Compute:** EC2 (Auto Scaling, Load Balancer)

**Database:** RDS (MySQL)

**Networking:** VPC, Public & Private Subnets, NAT Gateway, Internet Gateway, Route53

**Storage:** S3 (for Terraform backend state management)






## WorkFlow

1. Terraform Initialization: Configures the backend and initializes providers.

2. Networking Setup: Creates a VPC with public and private subnets, security groups, NAT gateway, internet gateway, and Route53 for DNS management.

3. Security & SSL: Implements ACM for SSL certificates and secures traffic with security groups.

4. Compute Layer: Deploys EC2 instances in an auto-scaling group behind an Application Load Balancer (ALB).

5. Database Layer: Sets up an RDS MySQL database in a private subnet to enhance security.

6. Provisioning & Deployment: Terraform applies configurations to deploy and manage infrastructure components efficiently.
## Deployment

To deploy this project

```bash
# Clone the repository
git clone https://github.com/Hrithik5/Terraform-Projects.git
cd Terraform-Projects/2tier

# Initialize Terraform
terraform init

# Plan the deployment
terraform plan

# Apply the changes
terraform apply -auto-approve
```


## Outputs

After deployment, Terraform provides key outputs such as:

Load Balancer DNS

Database Endpoint

Instance Details
## Cleanup

To destroy the infrastructure

```bash
terraform destroy -auto-approve
```

## Contributing

Contributions are always welcome!🥳

Feel free to fork this repo, submit issues, and contribute to improve functionality.


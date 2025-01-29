# Secure AWS ECS Flask Application with ALB & DynamoDB

![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)

A secure and scalable AWS architecture for deploying a Flask application using **ECS (Elastic Container Service)**, **DynamoDB**, and an **Application Load Balancer (ALB)**. Designed for high availability, fault tolerance, and compliance with AWS best practices.

---

## 📋 Overview
This project demonstrates a production-grade AWS setup to deploy a Flask application in a **secured ECS cluster**, integrated with DynamoDB for data persistence and an ALB for traffic distribution. Key features include:
- **Multi-AZ deployments** for high availability.
- **Private subnet isolation** for secure workloads.
- **VPC endpoints** for low-latency DynamoDB access.
- **IAM roles** enforcing least-privilege access.
- **Encryption** for data at rest and in transit.

---

## 🛠️ Tech Stack
- **Compute**: AWS ECS (Fargate), Docker, Flask  
- **Database**: DynamoDB  
- **Networking**: VPC, ALB, NAT Gateway, Public/Private Subnets  
- **Security**: IAM Roles, Security Groups, AWS KMS  
- **Infrastructure as Code (IaC)**: Terraform/CloudFormation  

---

## 📐 Architecture
![Architecture Diagram](https://github.com/user-attachments/assets/a006f3f6-39df-47fc-b18c-ae29f60bbec7)
 
**Key Components**:  
1. **VPC**: Segregated into public and private subnets.  
2. **ALB**: Routes external traffic to ECS containers in private subnets.  
3. **ECS Cluster**: Hosts Dockerized Flask app with auto-scaling.  
4. **DynamoDB**: Accessed securely via VPC endpoints.  
5. **NAT Gateway**: Enables private subnets to fetch updates securely.  

---

## 🔄 Workflow
1. **User Request**: Client sends a request to the ALB endpoint.  
2. **Traffic Routing**: ALB forwards requests to ECS tasks in private subnets.  
3. **Application Logic**: Flask app processes requests and interacts with DynamoDB.  
4. **Security**: IAM roles restrict database access; data encrypted end-to-end.  

---

## 🚀 Deployment
### Prerequisites:
- AWS CLI configured with credentials.
- Terraform/CloudFormation installed.

### Steps:
1. **Provision Infrastructure**:  
   ```bash
   terraform init && terraform apply  # Using Terraform

---
title: "Workshop"
date: 2024-01-01
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Deploy WEB_JENIKA on AWS Cloud

#### Overview

In this workshop, you will learn how to deploy the **WEB_JENIKA (CAFE_DI_ROM)** coffee shop management system on **Amazon Web Services (AWS)**. This hands-on lab guides you through the process of containerizing the application with Docker and running it on a single EC2 instance inside the AWS Default VPC to maximize cost savings within the AWS Free Tier.

The system is deployed using production-grade practices:
*   **Reverse Proxy & SSL**: Uses Nginx as a reverse proxy and Certbot Let's Encrypt to issue SSL certificates for the domain (`jenkam.site`).
*   **IAM Security**: Uses an IAM Instance Profile to grant permissions to the EC2 instance instead of hardcoding static credentials.
*   **Cloud Storage**: Integrates Amazon S3 to store invoice images uploaded via the OCR processing feature.
*   **Monitoring & Alerting**: Streams container logs directly from Docker to AWS CloudWatch Logs and configures AWS SNS to send automatic email alerts when the backend encounters system errors.

#### Links
*   **Resource (GitHub)**: [https://github.com/nguyennhatlong2309/APP_JENIKA.git](https://github.com/nguyennhatlong2309/APP_JENIKA.git)
*   **Production**: [https://jenkam.site](https://jenkam.site)

#### Content

1. [Workshop Overview](5.1-workshop-overview/)
2. [Prerequisites](5.2-prerequiste/)
3. [EC2 Launch & Environment Setup](5.3-s3-vpc/)
4. [Deploy Docker Compose & Database](5.4-s3-onprem/)
5. [Domain, SSL & Alerts Setup](5.5-policy/)
6. [Resource Cleanup](5.6-cleanup/)
---
title : "Introduction"
date : 2024-01-01 
weight : 1 
chapter : false
pre : " <b> 5.1. </b> "
---

#### WEB_JENIKA Web Platform
+ **WEB_JENIKA (WEB_CAFE)** is a comprehensive web-based coffee shop, inventory, and revenue management system. It is designed to work seamlessly alongside the **BrewMaster Pro (Java Swing Desktop App)** by sharing a single database.
+ The application features a modern, responsive user interface built using **Next.js (React 19)** with a premium **Glassmorphism** styling system, backed by a robust **Spring Boot 3.3** REST API.

#### Workshop Overview & Architecture
In this workshop, you will deploy the WEB_JENIKA application on AWS using a cost-effective, scalable, and highly available hybrid cloud architecture:
+ **Amazon EC2**: Used as the application host to run containerized services (Nginx Reverse Proxy, Next.js Frontend, Spring Boot Backend, and Hermes Agent) inside a unified Docker network.
+ **Amazon RDS (MySQL)**: Provides a managed database layer that mitigates Out-of-Memory (OOM) risks by offloading data storage from the small EC2 instance.
+ **Amazon S3**: Acts as a decoupled, durable object storage service to store invoice images uploaded via the OCR processing feature.
+ **AWS CloudWatch & SNS**: Leverages Docker's native `awslogs` driver to stream backend logs directly to CloudWatch, triggering instant email notifications through SNS when exceptions occur.

![overview](/images/5-Workshop/5.1-Workshop-overview/graph.jpeg)
---
title: "Proposal"
date: 2024-01-01
weight: 2
chapter: false
pre: " <b> 2. </b> "
---
# BrewMaster Pro & WEB_JENIKA (WEB_CAFE)  
## A Comprehensive Multi-Platform Coffee Shop Management Solution (Desktop & Web) Integrated with AWS Cloud  

### 1. Executive Summary  
The **BrewMaster Pro & WEB_JENIKA** project is designed to provide a comprehensive management solution for coffee shops, inventory, partners, employees, and revenue. The system integrates a desktop application (**Java Swing**) for on-site operations and a web application (**Next.js / React 19** with a **Spring Boot** backend) for remote administrators. Both platforms share a centralized MySQL database and leverage **Amazon Web Services (AWS)** (EC2, S3, CloudWatch, SNS) along with a custom domain `jenkam.site` (registered at Nhan Hoa) and DNS routing managed via **AWS Route 53** to ensure high availability, security, and low operational costs. All services (including the MySQL database) are deployed on a single EC2 virtual instance using Docker Compose.

In particular, to diversify and elevate the technical sophistication of the project, the system leverages the massive popularity of the **Hermes Agent** repository (GitHub: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent.git)) which currently boasts over 226k stars. Hermes Agent features the capability to learn, adapt, and grow smarter over time with usage. By utilizing free LLMs accessed through **OpenRouter**, the project configures a custom Skill for Hermes, enabling it to automatically create purchase or sales orders. Users can simply send invoice images through a configured chatbot (such as Telegram or Discord), which Hermes processes to extract data. To execute these operations securely, Hermes is granted a **special JWT (JSON Web Token)** that authorizes it to make write operations (POST requests) directly to the Spring Boot backend. Integrating this intelligent AI agent not only automates traditional manual data entry workflows but also diversifies the project architecture, showcasing the practical integration of cutting-edge AI Agent technologies.

### 2. Problem Statement  
*Current Situation & Issues*  
Many small coffee shops and retail outlets still manage their business data manually using **Excel** spreadsheets. This traditional approach introduces several severe challenges:
+ **Data Errors**: Manual data entry often leads to human errors in stock quantities, pricing calculations, and revenue reporting.
+ **Lack of Real-Time Sync**: Inventory, sales, and expense data are not synced in real-time across different branches or departments.
+ **Difficult Auditing**: Without a proper Activity Log, auditing transaction history and identifying revenue leakages is extremely difficult.
- **Risk of Data Loss**: Locally stored Excel sheets are vulnerable to file corruption, malware, or hardware failures, with no automated backup mechanisms.
- **Scalability Limitations**: Excel cannot support role-based user permissions, supplier debt tracking, or automated invoice processing using OCR technology.

*The Solution & User Requirements*  
To overcome these issues, the system introduces dedicated features and data forms tailored to the user's operational needs:
1. **Real-Time Dashboard**: Visualizes revenue, operational expenses, and profits using interactive charts (daily/monthly/yearly).
2. **Sales Orders Form**: Facilitates fast customer checkout, product search, and membership discount calculations.
3. **Purchase Orders Form**: Tracks raw materials and equipment intake, supplier debts, and transaction history.
4. **Inventory Management Form**: Tracks real-time stock levels and trigger automated alerts when stock drops below threshold levels.
5. **Expense Tracking Form**: Logs daily operational costs such as electricity, water bills, rent, and staff salaries.
6. **Partner Management Form**: Manages and categorizes customer loyalty accounts and supplier details.
7. **Staff Management & Flexible Permissions**: Oversees detailed employee information and implements a flexible role-based access control system (Admin, Manager, Cashier, Stockkeeper) to grant or restrict access to specific business forms and sensitive data.
8. **OCR Invoice Integration with S3**: Uploads raw invoice images to Amazon S3 and uses OCR to extract invoice data for automated inventory entry.
9. **Activity Log Management Page**: Logs and audits the complete history of operations and system actions previously performed by all users, ensuring high traceability, easier auditing, and transparency.

### 3. Solution Architecture  
The platform is built on a production-ready AWS infrastructure:
- **Client Tier**: Users access the Next.js Web App via browser or run the Java Swing Desktop App connected to the database.
- **Application & Database Tier (Amazon EC2)**: Hosts Nginx (Reverse Proxy & SSL), Next.js Frontend, Spring Boot Backend, and the MySQL database container inside a Docker network via Docker Compose.
- **Storage Tier (Amazon S3)**: Provides durable and unlimited storage for OCR invoice images.
- **Performance Optimization Tier**: Configures a **2GB Swap File** on the EC2 instance to serve as virtual RAM, preventing Out-of-Memory (OOM) errors for the MySQL database when running concurrently with application components.
- **Monitoring & Alerting**: Streams container logs directly to **AWS CloudWatch** using Docker's native `awslogs` driver, triggering email alerts via **AWS SNS** upon system exceptions.

![WEB_JENIKA Architecture](/images/5-Workshop/5.1-Workshop-overview/graph.jpeg)

*AWS Services & Network Solution Used*  
- **Amazon EC2**: Hosts the entire containerized system (Next.js, Spring Boot, MySQL, Nginx) on a single virtual instance (`t3.micro`), supported by a 2GB Swap File.
- **Amazon S3**: Stores original invoice images for OCR processing.
- **DNS & Domain (Nhan Hoa & AWS Route 53)**: Utilizes a custom domain `jenkam.site` registered at Nhan Hoa (~$2.00/year), routed through AWS Route 53 to resolve the domain to the EC2 instance's Elastic IP.
- **AWS CloudWatch**: Collects logs and filters errors from the Backend container.
- **AWS SNS**: Delivers instant email notifications to developers when errors occur.

### 4. Technical Implementation  
*Implementation Phases*  
The project is divided into four key stages:
1. **Phase 1 (Weeks 1 - 3)**: Project kickoff, research AWS services, adjust project plans, design database schemas, and initialize local development environments (boilerplates).
2. **Phase 2 (Weeks 4 - 5)**: Develop core backend API endpoints (Spring Boot), build frontend user interfaces (Next.js), and integrate AWS SDK (S3, OCR).
3. **Phase 3 (Weeks 6 - 7)**: Package applications via Docker, deploy containerized environments to AWS EC2, configure Nginx Reverse Proxy with SSL, import database, and set up CloudWatch Logs + AWS SNS monitoring.
4. **Phase 4 (Weeks 8 - 9)**: Run real-world testing (Demo), collect user feedback to fix UI/UX issues, complete bilingual reports on Hugo, and submit the draft to the Mentor for approval.

### 5. Timeline & Milestones  
- **Weeks 1-3**: Onboard with the company, attend Event 1, self-study AWS services, adjust project scope, design database schema, and set up local boilerplates.
- **Weeks 4-5**: Implement core business APIs and Next.js interfaces, configure AWS SDK for S3 uploading, and integrate OCR service for raw invoices.
- **Weeks 6-7**: Containerize application components, deploy to AWS EC2 (including MySQL container) via Docker Compose, set up Let's Encrypt SSL via Nginx, import MySQL data, and configure CloudWatch & SNS monitoring.
- **Weeks 8-9**: Deploy a live Demo, gather staff feedback for UI/UX enhancements, consolidate reports in bilingual format on Hugo, and submit the final draft to the Mentor.

### 6. Budget Estimation  
By utilizing the **AWS Free Tier (First 12 Months)**, operational costs are minimized, as detailed in the table below:

| Service / Resource | Tier Applied | Cost (First 12 Months) | Cost (From Month 13) | Details / Free Limit |
| --- | --- | --- | --- | --- |
| **Amazon EC2** | AWS Free Tier | $0.00/month | ~$5.00/month | `t3.micro` configuration, free 750 hours/month. (Runs Nginx, Next.js, Spring Boot, MySQL). |
| **Amazon S3** | AWS Free Tier | $0.00/month | ~$0.50/month | Free up to 5GB of storage. |
| **AWS CloudWatch & SNS** | AWS Free Tier | $0.00/month | ~$0.50/month | Free 5GB of log ingestion and 1,000,000 email messages/month. |
| **Domain & Route 53** | Custom Domain | ~$0.66/month | ~$0.66/month | Custom domain `jenkam.site` registered at Nhan Hoa (~$2.00/year, or ~$0.16/month) and AWS Route 53 Hosted Zone fee ($0.50/month). |
| **Total** | | **~$0.66/month** | **~$6.66/month** | **Highly cost-effective due to resource optimization.** |

### 7. Risk Assessment  
*Risk Matrix*  
- **Out of Memory (OOM) on EC2**: High impact, medium probability.  
- **Data Loss**: Critical impact, low probability.  
- **Infrastructure Connection Issues**: Medium impact, medium probability.  

*Mitigation & Contingency Plans*  
- **Mitigating OOM**: Configured a **2GB Swap File** on the EC2 host as virtual memory to support the 1GB of physical RAM when running MySQL, Spring Boot, and Next.js concurrently.
- **Mitigating Data Loss**: Persisted MySQL data using a **Docker Volume** mapped to the host directory and set up periodic manual/automated database dumps (SQL files) to Amazon S3 or external storage.
- **Mitigating Connectivity Errors**: Utilized Nginx reverse proxy routing with precise logs stream, and created CloudWatch Alarms to trigger SNS email alerts immediately upon Backend failures.

### 8. Expected Outcomes  
- **Digital Transformation**: Replaced manual Excel workflow with a centralized, automated, and accurate database management solution.
- **Improved Operational Efficiency**: Reduced order checkout, purchase tracking, and accounting time by up to 70%.
- **Reliable Data & Security**: Business data and invoice assets are secured in AWS cloud with granular access controls and periodic backups.
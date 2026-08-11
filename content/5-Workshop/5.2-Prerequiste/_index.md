---
title : "Prerequiste"
date : 2024-01-01 
weight : 2
chapter : false
pre : " <b> 5.2. </b> "
---

#### 1. Local Prerequisites
To build, package the application into Docker images, and connect to cloud resources, prepare the following tools on your local machine:
*   **Java Development Kit (JDK) 17**: Required version to run the desktop application and backend API.
*   **Apache Maven**: Used for managing dependencies and compiling the Java/Spring Boot project.
*   **Node.js (v18+)**: Used to install dependencies and run the Next.js Frontend.
*   **Git & SSH Client**: Required to clone the repository and securely SSH into the EC2 instance.
*   **Docker & Docker Desktop**: Used to build Docker images (`helios2309/cafe-backend:latest`, `helios2309/cafe-frontend:latest`) locally and push them to Docker Hub before pulling them on the EC2 instance.
*   **Docker Hub Account**: Used to store the project's Docker images (e.g. account: `helios2309`).

---

#### 2. IAM Permissions
Ensure your AWS IAM User account has sufficient permissions to provision and cleanup resources in this workshop. Attach the following policy to your account:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "JenkamWorkshopPermissions",
            "Effect": "Allow",
            "Action": [
                "cloudformation:*",
                "ec2:*",
                "s3:*",
                "iam:CreateRole",
                "iam:DeleteRole",
                "iam:GetRole",
                "iam:PassRole",
                "iam:PutRolePolicy",
                "iam:DeleteRolePolicy",
                "iam:GetRolePolicy",
                "iam:CreateInstanceProfile",
                "iam:DeleteInstanceProfile",
                "iam:GetInstanceProfile",
                "iam:AddRoleToInstanceProfile",
                "iam:RemoveRoleFromInstanceProfile",
                "logs:*",
                "cloudwatch:*",
                "sns:*",
                "route53:*"
            ],
            "Resource": "*"
        }
    ]
}
```

---

#### 3. Provision Base Infrastructure using AWS Console
Since the entire system (Next.js Frontend, Spring Boot Backend, MySQL Database, and Nginx) will be deployed together on a single EC2 virtual instance using Docker Compose, we will leverage the **Default VPC** automatically provided by AWS and manually create the following auxiliary resources:

##### 3.1. Provision EC2 Security Group (`web-app-sg`)
To allow SSH connections and public web traffic:
1. Log in to the AWS Management Console and switch to the **Sydney region (`ap-southeast-2`)**.

   ![Create Security Group](/images/5-Workshop/5.2-Prerequisite/5.2_3.1.1.png)

2. Search for the **EC2** service -> Select **Security Groups** on the left menu -> Click **Create security group**.
3. Configure basic information:
   * **Security group name**: `web-app-sg`
   * **Description**: `Allow SSH, HTTP, and HTTPS access to EC2`
   * **VPC**: Select the **Default VPC** of the Sydney region.
4. In the **Inbound rules** section, add the following 3 rules:
   * **Rule 1**: Type `SSH` (Port 22) -> Source: Select `My IP` (or `Anywhere-IPv4` - `0.0.0.0/0` to allow connection from any network).
   * **Rule 2**: Type `HTTP` (Port 80) -> Source: Select `Anywhere-IPv4` (`0.0.0.0/0`).
   * **Rule 3**: Type `HTTPS` (Port 443) -> Source: Select `Anywhere-IPv4` (`0.0.0.0/0`).
5. Scroll down and click **Create security group**. Record the newly created Security Group ID (e.g., `sg-0123456789abcdef0`).

   ![Security Group Inbound Rules](/images/5-Workshop/5.2-Prerequisite/5.2_3.1.234.png)


##### 3.2. Provision Amazon S3 Bucket (`jenkam-images`)
To store invoice image files for the OCR processing feature:
1. Search for and select the **S3** service on the AWS Console -> Click **Create bucket**.
2. Configure settings:
   * **Bucket name**: Enter a globally unique name (e.g., `jenkam-images`).
   * **AWS Region**: Select **ap-southeast-2** (Sydney) to match your EC2 instance's region.
3. In the **Block Public Access settings for this bucket** section: Keep the default **Block all public access** setting to ensure internal data security.
4. Scroll to the bottom of the page and click **Create bucket**.
5. **Create folder structure (Folders):**
   * Access the newly created `jenkam-images` bucket -> Click **Create folder**.
   * Create the first folder: Name it `invoices` (for storing invoice images permanently). Click **Create folder**.
   * Create the second folder: Name it `temp` (for temporary files generated during OCR processing). Click **Create folder**.

   ![S3 Bucket Folders](/images/5-Workshop/5.2-Prerequisite/5.2_3.2.12345.png)

6. **Configure Lifecycle Rule for the `temp` folder:**
   To automatically clean up temporary image files and optimize storage capacity and costs:
   * Navigate to the **Management** tab of the bucket -> Under **Lifecycle rules**, click **Create lifecycle rule**.
   * Configure the rule:
     * **Lifecycle rule name**: `CleanTempFolder`
     * **Rule scope**: Select **Limit the scope of this rule using one or more filters**.
     * **Prefix**: Enter `temp/` (make sure to include the trailing slash `/` to apply specifically to objects inside the `temp` folder).
     * **Lifecycle rule actions**: Tick **Expire current versions of objects**.
     * **Expire current versions of objects**: In the **Days after object creation** field, enter `1` (objects in the `temp` folder will be deleted automatically 24 hours after upload).
   * Click **Create rule** to finish.

   ![S3 Lifecycle Rule](/images/5-Workshop/5.2-Prerequisite/5.2_3.2.6.png)



##### 3.3. Provision IAM Role for EC2 (`Jenkam-EC2-Role`)
Grants secure permissions for the EC2 instance to communicate with S3 and stream Docker logs directly to CloudWatch Logs:
1. Search for the **IAM** service on the AWS Console -> Select **Roles** on the left menu -> Click **Create role**.
2. Select **Trusted entity type**: **AWS service** -> Select **EC2** as the service use case. Click **Next**.
3. On the **Add permissions** page, search for and select the following two managed policies:
   * `AmazonS3FullAccess` (or create a Custom Policy restricting access only to the `jenkam-images` bucket).
   * `CloudWatchLogsFullAccess` (allows streaming logs from the Docker backend to CloudWatch).
4. Click **Next**. Set the identifying info:
   * **Role name**: `Jenkam-EC2-Role`
5. Click **Create role**. The system will automatically create an **Instance Profile** with the same name, which you can attach to your EC2 instance during launch.

   ![IAM Role Creation](/images/5-Workshop/5.2-Prerequisite/5.2_3.3.png)

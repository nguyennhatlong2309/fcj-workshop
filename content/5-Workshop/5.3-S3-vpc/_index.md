---
title : "EC2 Launch & Environment Setup"
date : 2024-01-01 
weight : 3
chapter : false
pre : " <b> 5.3. </b> "
---

In this section, we will launch an Amazon EC2 instance in the **Sydney region (ap-southeast-2)**, configure a 2 GB Swap File for virtual RAM, and install Docker/Docker Compose to prepare the hosting environment for JENKAM.

---

#### 1. Launch EC2 Instance & Associate Elastic IP
To host our web services, we will deploy an Ubuntu Server virtual machine:

##### Steps to Launch EC2 Instance:
1. Log in to the AWS Management Console and select the **Sydney** region.
2. Search for the **EC2** service -> Select **Instances** on the left menu -> Click **Launch instances**.
3. Configure the server settings:
   *   **Name**: `cafe-app-server`
   *   **Application and OS Images (AMI)**: Choose **Ubuntu** (Ubuntu Server 22.04 LTS, 64-bit x86).
   *   **Instance type**: Choose **`t3.micro`** (or `t2.micro` depending on which is available under the Free Tier in your region).
   *   **Key pair (login)**: Select your existing `.pem` key or create a new one to download (e.g., `dashboard_manage_coffe.pem`) for SSH authentication.
   *   **Network settings**:
       *   Select **Select existing security group** and check the **`web-app-sg`** security group created in Section 5.2.
   *   **Advanced details**:
       *   **IAM instance profile**: Choose **`Jenkam-EC2-InstanceProfile`** (automatically created via the `Jenkam-EC2-Role` in Section 5.2 to grant S3 and CloudWatch permissions to the server).
4. Click **Launch instance** and wait about 1 minute for the instance to boot.

   ![Launch EC2 and Associate Elastic IP](/images/5-Workshop/5.3-S3-vpc/5.3.1.2.png)

##### Allocate & Associate Elastic IP (Static IP):
By default, the public IP of an EC2 instance changes whenever the instance is stopped and restarted. We need to allocate a static Elastic IP to keep the address persistent for our custom domain:
1. In the EC2 Console, select **Elastic IPs** from the left menu -> Click **Allocate Elastic IP address**.
2. Click **Allocate** to request a new static IP address.
3. Check the allocated IP address -> Click **Actions** -> Select **Associate Elastic IP address**.
4. In the **Instance** field, select your newly launched `cafe-app-server`. Click **Associate** to confirm.



---

#### 2. Configure a 2 GB Swap File (Virtual RAM)
The AWS Free Tier EC2 instance (`t3.micro`) only provides **1 GB of physical RAM**. Running MySQL Database, Spring Boot Backend, and Next.js Frontend simultaneously will overload the system, resulting in **Out Of Memory (OOM)** errors that terminate the database container. To prevent this, we will configure a **2 GB Swap File** on the SSD as virtual RAM.

1. Open a terminal on your local machine and connect to your EC2 instance via SSH (replace the IP address with your Elastic IP):
   ```bash
   ssh -i "dashboard_manage_coffe.pem" ubuntu@your-ec2-elastic-ip
   ```
2. Execute the following commands in sequence to create and activate the Swap File:
   ```bash
   # 1. Create an empty swap file of 2GB capacity
   sudo fallocate -l 2G /swapfile

   # 2. Restrict read/write permissions to root only for security
   sudo chmod 600 /swapfile

   # 3. Format the file as Swap space
   sudo mkswap /swapfile

   # 4. Enable the swap file in the system
   sudo swapon /swapfile

   # 5. Append configuration to fstab to auto-activate Swap on EC2 boot
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```
3. Check the memory allocation to verify that Swap has been successfully enabled:
   ```bash
   free -h
   ```
   *Actual command output from your EC2 server while the system is running:*
   ```text
   ubuntu@ip-172-31-10-185:~/cafe-app$ free -h
                  total        used        free      shared  buff/cache   available
   Mem:           908Mi       624Mi        74Mi       2.1Mi       324Mi       284Mi
   Swap:          2.0Gi       678Mi       1.3Gi
   ```
   *Real-world Observation:* The server is currently utilizing `624Mi` of physical RAM for the operating system and Docker containers, and has automatically offloaded `678Mi` of memory load onto the virtual **Swap space**. Without this 2 GB Swap File configuration, the Free Tier EC2 instance (which only has 1 GB of physical RAM) would have run out of memory, causing an Out of Memory (OOM) crash that would immediately terminate the MySQL Database or Spring Boot backend processes.


---

#### 3. Install Docker & Docker Compose
Docker allows containerizing and running Next.js, Spring Boot, MySQL, and Nginx independently and consistently on the EC2 host.

1. Update system packages and install Docker:
   ```bash
   # Update package lists
   sudo apt update && sudo apt upgrade -y

   # Install Docker and Docker Compose V2
   sudo apt install docker.io docker-compose-v2 -y
   ```
2. Add the current user (`ubuntu`) to the `docker` group to run docker commands without needing `sudo` prefix:
   ```bash
   sudo usermod -aG docker $USER
   
   # Apply the new permissions to the current shell session
   newgrp docker
   ```
   *Verify that the `ubuntu` user has been successfully added to the `docker` group:*
   ```bash
   groups
   ```
   *Actual command output displayed on your EC2 server:*
   ```text
   ubuntu@ip-172-31-10-185:~/cafe-app$ groups
   ubuntu adm cdrom sudo dip plugdev lxd default-ec2-users docker
   ```

3. Verify the installation by checking the versions:
   ```bash
   docker --version
   docker compose version
   ```
   *Actual command outputs displayed on your EC2 server:*
   ```text
   ubuntu@ip-172-31-10-185:~/cafe-app$ docker --version
   Docker version 29.1.3, build 29.1.3-0ubuntu4.1

   ubuntu@ip-172-31-10-185:~/cafe-app$ docker compose version
   Docker Compose version v2.29.1
   ```
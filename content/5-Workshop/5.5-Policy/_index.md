---
title : "Domain, SSL & Alerts Setup"
date : 2024-01-01 
weight : 5
chapter : false
pre : " <b> 5.5. </b> "
---

In this section, we will configure the custom domain link, set up the SSL (HTTPS) certificate for the system using Certbot Let's Encrypt, and establish an automated error notification pipeline using AWS CloudWatch Logs & AWS SNS.

---

#### 1. Configure Domain and Obtain Free SSL Certificate
The **WEB_JENIKA** platform uses the custom domain **`jenkam.site`**.

##### Execution Steps:
1. **Link Route 53 Name Servers (NS) with Domain Registrar:**
   * Log in to the AWS Console, search for the **Route 53** service -> Select **Hosted zones** on the left menu -> Click **Create hosted zone**.
   * Configure settings:
     * **Domain name**: `jenkam.site`
   * Click **Create hosted zone**. Once successfully created, Route 53 will automatically assign a set of 4 **Name Servers (NS)** records (e.g., `ns-xxx.awsdns-xx.com`, `ns-xxx.awsdns-xx.org`, ...). Copy these 4 server addresses.
   * Log in to the control panel of the domain registrar where you purchased `jenkam.site` (such as Nhan Hoa, Namecheap, GoDaddy, etc.).
   * Select your domain settings, find the **Name Servers** configuration -> Switch from the default to **Custom DNS (or Custom Name Servers)** and paste the 4 Route 53 NS addresses you copied. Click Save.

   ![Configure Hosted Zone Route 53](/images/5-Workshop/5.5-Policy/5.5.1_1.png)

2. **Create A Records Pointing to the EC2 Instance:**
   * Return to your hosted zone for `jenkam.site` in the Route 53 Console -> Click **Create record**.
   * Create the A record for the root domain:
     * **Record name**: Leave blank.
     * **Record type**: Select `A - Routes traffic to an IPv4 address and some AWS resources`.
     * **Value**: Enter the static Elastic IP address of your EC2 instance.
   * Click **Create records**.
   * Create the A record for the `www` domain: Click **Create record** -> Enter **Record name** as `www` -> Select **Record type** as `A` -> Enter the same Elastic IP address of the EC2 instance in the **Value** field -> Click **Create records**.

   ![A Records and Name Servers Configuration](/images/5-Workshop/5.5-Policy/5.5.1_2.png)

3. **Install and Generate SSL Certificate using Certbot Let's Encrypt:**
   * In your EC2 terminal, temporarily stop the Nginx container (as Certbot needs to bind to port 80 to verify domain ownership):
     ```bash
     docker stop cfe_di_rom_nginx
     ```
   * Install Certbot and request the SSL certificate for your domains:
     ```bash
     # Update packages and install Certbot
     sudo apt update
     sudo apt install certbot -y

     # Run Certbot in standalone mode to request certificates for both root and www domains
     sudo certbot certonly --standalone -d jenkam.site -d www.jenkam.site
     ```
     *Note:* Once successfully generated, the SSL certificates will be saved in the directory `/etc/letsencrypt/live/jenkam.site/`.



---

#### 2. Configure Nginx for HTTPS (Port 443)
Once the SSL certificate is generated, we upgrade the Nginx configuration to automatically redirect all insecure HTTP requests (port 80) to secure HTTPS (port 443).

1. Edit the Nginx configuration file on EC2:
   `nano ~/cafe-app/nginx/conf.d/default.conf`
2. Replace its entire content with the following SSL configuration:
   ```nginx
   server {
       listen 80;
       server_name jenkam.site www.jenkam.site;
       return 301 https://$host$request_uri; # Redirect HTTP to HTTPS
   }

   server {
       listen 443 ssl;
       server_name jenkam.site www.jenkam.site;

       # Path to SSL Let's Encrypt certificates (mounted from EC2 into the container)
       ssl_certificate /etc/letsencrypt/live/jenkam.site/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/jenkam.site/privkey.pem;

       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers HIGH:!aNULL:!MD5;

       # Route Spring Boot Backend APIs
       location /api/ {
           proxy_pass http://backend:8080/api/v1/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       # Route Next.js Frontend
       location / {
           proxy_pass http://frontend:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
3. Restart the container stack to apply the new Nginx configuration:
   ```bash
   cd ~/cafe-app
   docker compose up -d
   ```
   *You can now securely access the system at **`https://jenkam.site`**.*

---

#### 3. Set Up Automated Error Alerts (AWS CloudWatch & SNS Alerts)
In the `docker-compose.yml` file, the Spring Boot backend service is configured to ship its system logs directly to CloudWatch Logs under the log group `cfe-di-rom-logs`. We will now configure CloudWatch to trigger instant email alerts for developers when system errors occur.

##### Step 3.1: Create an SNS Topic for Email Notifications
1. Navigate to the **Amazon SNS Console** -> Select **Topics** -> Click **Create topic**.
2. Select the **Standard** type, and enter the name `cfe-di-rom-alerts`. Click **Create topic**.
3. Click on the newly created Topic -> Click **Create subscription**.
4. Configure the subscription settings:
   *   **Protocol**: Select **Email**.
   *   **Endpoint**: Enter your personal email address to receive the alerts.
5. Click **Create subscription**.
6. **Confirm the Subscription:** Open your email inbox, find the mail with the subject *AWS Notification - Subscription Confirmation*, and click the **Confirm Subscription** link to verify.

   ![SNS Topic Configuration](/images/5-Workshop/5.5-Policy/5.5.3_buoc3.1.png)

##### Step 3.2: Set Up a Metric Filter on CloudWatch Logs
1. Navigate to the **CloudWatch Console** -> Select **Log groups** on the left menu -> Click the log group **`cfe-di-rom-logs`**.
2. Select the **Metric filters** tab -> Click **Create metric filter**.
3. Configure the Filter:
   *   **Filter pattern**: Enter `?ERROR ?Exception` (to match log lines containing the keywords ERROR or Exception).
   *   **Metric name**: `BackendErrorCount`
4. Click **Save metric filter**.

   ![Metric Filter Configuration](/images/5-Workshop/5.5-Policy/5.5.3_buoc3.2.png)

##### Step 3.3: Create a CloudWatch Alarm
1. Click on the newly created `BackendErrorCount` Metric filter -> Click **Create alarm**.
2. Configure the Alarm conditions:
   *   **Statistic**: Select `Sum`.
   *   **Period**: Select `1 minute`.
   *   **Whenever BackendErrorCount is...**: Select `Greater than or equal to 1` (alarms if 1 or more errors appear within a 1-minute window).
3. Configure Actions:
   *   Under **Notification**, choose the **In alarm** state trigger.
   *   Select to send notifications to the **`cfe-di-rom-alerts`** SNS Topic created in Step 3.1.
4. Name the Alarm `Backend-Logic-Error-Alarm` -> Click **Create alarm**.
   *Whenever the Spring Boot backend experiences a logic error or OOM crash that triggers an ERROR log, AWS will automatically send a notification email directly to your inbox.*

   ![CloudWatch Alarm Configuration](/images/5-Workshop/5.5-Policy/5.5.3_buoc3.3.png)


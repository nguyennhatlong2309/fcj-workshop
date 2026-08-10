---
title : "Deploy Docker Compose & Database"
date : 2024-01-01 
weight : 4
chapter : false
pre : " <b> 5.4. </b> "
---

In this section, we will create the **Docker Compose** configuration file, set up the **Nginx Reverse Proxy**, launch all services on the EC2 host, and import the initial MySQL database.

---

#### 1. Create Directory Structure and Prepare Files
On your EC2 host, navigate to the user directory and create the folders for the configurations:
```bash
# Create project directory and Nginx configuration folder
mkdir -p ~/cafe-app/nginx/conf.d
```

---

#### 2. Write the `docker-compose.yml` File
This Docker Compose configuration file defines 4 core services:
1.  **mysql**: MySQL 8.0 relational database, with data persisted via a Docker Volume.
2.  **backend**: Spring Boot 3.3 REST API connected to MySQL, streaming logs to CloudWatch.
3.  **frontend**: Next.js user interface running on port 3000.
4.  **nginx**: Web server accepting external traffic (port 80/443) and proxying it to the Frontend and Backend.

Create the file `~/cafe-app/docker-compose.yml` on the EC2 instance with the following content:
```yaml
version: "3.8"

services:
  mysql:
    image: mysql:8.0
    container_name: cfe_di_rom_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: Admin2309@@
      MYSQL_DATABASE: cfe_di_rom
      MYSQL_USER: cafe_user
      MYSQL_PASSWORD: Admin2309@@
    volumes:
      - mysql_data:/var/lib/mysql
    expose:
      - "3306"
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_general_ci

  backend:
    image: helios2309/cafe-backend:latest
    container_name: cfe_di_rom_backend
    restart: always
    depends_on:
      - mysql
    logging:
      driver: "awslogs"
      options:
        awslogs-group: "cfe-di-rom-logs"
        awslogs-region: "ap-southeast-2"   # Your Sydney region
        awslogs-stream: "backend"
        awslogs-create-group: "true"
    environment:
      - SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/cfe_di_rom?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
      - SPRING_DATASOURCE_USERNAME=cafe_user
      - SPRING_DATASOURCE_PASSWORD=Admin2309@@
      - AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
      - AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
      - AWS_S3_BUCKET=jenkam-images
      - AWS_REGION=ap-southeast-2
    expose:
      - "8080"

  frontend:
    image: helios2309/cafe-frontend:latest
    container_name: cfe_di_rom_frontend
    restart: always
    environment:
      - NEXT_PUBLIC_API_URL=https://jenkam.site/api
    expose:
      - "3000"


  nginx:
    image: nginx:alpine
    container_name: cfe_di_rom_nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - frontend
      - backend

volumes:
  mysql_data:
```

---

#### 3. Set Up Nginx Configuration File
Nginx acts as a Reverse Proxy that listens on the HTTP port (80) and forwards incoming traffic to the appropriate Frontend (Next.js) or Backend (Spring Boot) container.

Create the file `~/cafe-app/nginx/conf.d/default.conf` with the following basic routing configuration:
```nginx
server {
    listen 80;
    server_name jenkam.site www.jenkam.site;

    # Route for Backend Spring Boot APIs
    location /api/ {
        proxy_pass http://backend:8080/api/v1/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Default route for Next.js Frontend
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```

---

#### 4. Launch the Docker Containers
From the directory containing the `docker-compose.yml` file on your EC2 instance, run the start command in detached mode:
```bash
cd ~/cafe-app
docker compose up -d
```

Verify that all containers are running successfully:
```bash
docker ps
```
*Ensure all 4 containers (`cfe_di_rom_db`, `cfe_di_rom_backend`, `cfe_di_rom_frontend`, `cfe_di_rom_nginx`) display an `Up` status.*

---

#### 5. Import the Initial Database Schema
To populate the database so the application can run immediately, import the SQL data dump into the MySQL container:

1. **From your local machine's terminal**, upload the SQL data file (`import_data.sql` or `init.sql`) to your EC2 instance:
   ```bash
   scp -i "dashboard_manage_coffe.pem" import_data.sql ubuntu@your-ec2-elastic-ip:~/cafe-app/
   ```
2. **From your EC2 terminal window**, import the uploaded SQL file directly into the MySQL container:
   ```bash
   docker exec -i cfe_di_rom_db mysql -uroot -pAdmin2309@@ cfe_di_rom < ~/cafe-app/import_data.sql
   ```
3. **Verify the import result:**
   Access the database directly to count the number of users to confirm a successful import:
   ```bash
   docker exec -it cfe_di_rom_db mysql -uroot -pAdmin2309@@ cfe_di_rom -e "SHOW TABLES; SELECT COUNT(*) FROM users;"
   ```

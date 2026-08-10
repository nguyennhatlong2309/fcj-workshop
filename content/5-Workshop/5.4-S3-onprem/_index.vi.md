---
title : "Triển khai Docker Compose và Cơ sở dữ liệu"
date : 2024-01-01 
weight : 4
chapter : false
pre : " <b> 5.4. </b> "
---

Trong phần này, chúng ta sẽ thực hiện viết tệp tin cấu hình **Docker Compose**, thiết lập **Nginx Reverse Proxy**, khởi chạy toàn bộ các dịch vụ trên EC2 và thực hiện nạp cơ sở dữ liệu MySQL ban đầu.

---

#### 1. Tạo cấu trúc thư mục và chuẩn bị tệp tin
Trên máy chủ EC2, di chuyển về thư mục người dùng và tạo thư mục chứa cấu hình:
```bash
# Tạo thư mục dự án và thư mục cấu hình Nginx
mkdir -p ~/cafe-app/nginx/conf.d
```

---

#### 2. Soạn thảo tệp tin `docker-compose.yml`
Tệp cấu hình Docker Compose này sẽ định nghĩa 4 dịch vụ chính:
1.  **mysql**: Cơ sở dữ liệu MySQL 8.0, dữ liệu được ghi lâu bền qua Docker Volume.
2.  **backend**: API Spring Boot 3.3 kết nối đến MySQL, đẩy logs lên CloudWatch.
3.  **frontend**: Giao diện Next.js chạy ở cổng 3000.
4.  **nginx**: Máy chủ web nhận lưu lượng ngoài (cổng 80/443) để điều hướng về Frontend và Backend.

Hãy tạo tệp tin `~/cafe-app/docker-compose.yml` trên EC2 với nội dung sau:
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
        awslogs-region: "ap-southeast-2"   # Vùng Sydney của bạn
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

#### 3. Thiết lập tệp cấu hình Nginx
Nginx sẽ làm nhiệm vụ lắng nghe các kết nối từ cổng HTTP (80) và chuyển tiếp lưu lượng tương ứng về đúng container Frontend (Next.js) hoặc Backend (Spring Boot).

Hãy tạo tệp tin `~/cafe-app/nginx/conf.d/default.conf` với cấu hình định tuyến cơ bản ban đầu:
```nginx
server {
    listen 80;
    server_name jenkam.site www.jenkam.site;

    # Định tuyến cho các API Backend Spring Boot
    location /api/ {
        proxy_pass http://backend:8080/api/v1/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Định tuyến mặc định cho Next.js Frontend
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

#### 4. Khởi chạy các Docker Container
Tại thư mục chứa file `docker-compose.yml` trên EC2, chạy lệnh khởi động ở chế độ chạy ngầm (detached mode):
```bash
cd ~/cafe-app
docker compose up -d
```

Kiểm tra trạng thái hoạt động của các container:
```bash
docker ps
```
*Đảm bảo cả 4 container (`cfe_di_rom_db`, `cfe_di_rom_backend`, `cfe_di_rom_frontend`, `cfe_di_rom_nginx`) đều hiển thị trạng thái `Up`.*

---

#### 5. Import dữ liệu ban đầu vào MySQL
Để ứng dụng có cơ sở dữ liệu hoạt động ngay lập tức, chúng ta nạp file script sql ban đầu vào MySQL container:

1. **Từ terminal máy cá nhân của bạn**, upload file dữ liệu (`import_data.sql` hoặc `init.sql`) lên thư mục ứng dụng trên EC2:
   ```bash
   scp -i "dashboard_manage_coffe.pem" import_data.sql ubuntu@your-ec2-elastic-ip:~/cafe-app/
   ```
2. **Từ cửa sổ terminal EC2**, import tệp SQL vừa tải lên trực tiếp vào trong container MySQL:
   ```bash
   docker exec -i cfe_di_rom_db mysql -uroot -pAdmin2309@@ cfe_di_rom < ~/cafe-app/import_data.sql
   ```
3. **Kiểm tra kết quả nạp dữ liệu:**
   Truy cập trực tiếp vào DB để đếm số lượng người dùng nhằm xác nhận import thành công:
   ```bash
   docker exec -it cfe_di_rom_db mysql -uroot -pAdmin2309@@ cfe_di_rom -e "SHOW TABLES; SELECT COUNT(*) FROM users;"
   ```

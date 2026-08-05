---
title : "Cấu hình Tên miền, SSL & Cảnh báo lỗi tự động"
date : 2024-01-01 
weight : 5
chapter : false
pre : " <b> 5.5. </b> "
---

Trong phần này, chúng ta sẽ cấu hình liên kết tên miền DDNS, thiết lập chứng chỉ bảo mật SSL (HTTPS) cho hệ thống thông qua Certbot Let's Encrypt và cấu hình hệ thống cảnh báo lỗi tự động qua AWS CloudWatch Logs & AWS SNS.

---

#### 1. Cấu hình tên miền và Cấp chứng chỉ SSL miễn phí
Hệ thống **WEB_JENIKA** sử dụng tên miền riêng **`jenkam.site`**.

##### Các bước thực hiện:
1. **Liên kết Name Servers (NS) của Route 53 với Nhà đăng ký tên miền:**
   * Truy cập AWS Console, tìm kiếm dịch vụ **Route 53** -> Chọn **Hosted zones** ở thanh bên trái -> Click **Create hosted zone**.
   * Thiết lập thông tin:
     * **Domain name**: `jenkam.site`
   * Bấm **Create hosted zone**. Sau khi khởi tạo thành công, Route 53 sẽ tự động cấp một bộ gồm 4 dòng bản ghi máy chủ tên miền **Name Servers (NS)** (ví dụ: `ns-xxx.awsdns-xx.com`, `ns-xxx.awsdns-xx.org`,...). Hãy sao chép 4 dòng địa chỉ này.
   * Đăng nhập vào trang quản trị của nhà đăng ký tên miền nơi bạn mua `jenkam.site` (như Namecheap, GoDaddy, Mắt Bão,...).
   * Chọn cấu hình tên miền của bạn, tìm mục **Name Servers** (Máy chủ tên miền) -> Chuyển từ chế độ mặc định sang **Custom DNS (hoặc Custom Name Servers)** và dán 4 dòng địa chỉ NS của Route 53 vừa sao chép vào. Nhấn Lưu lại.

   ![Cấu hình Hosted Zone Route 53](/images/5-Workshop/5.5-Policy/5.5.1_1.png)

2. **Khởi tạo các bản ghi A trỏ về máy chủ EC2:**
   * Quay lại màn hình Hosted Zone `jenkam.site` trên Route 53 Console -> Click **Create record**.
   * Tạo bản ghi A cho tên miền gốc:
     * **Record name**: Để trống.
     * **Record type**: Chọn `A - Routes traffic to an IPv4 address and some AWS resources`.
     * **Value**: Nhập địa chỉ Elastic IP tĩnh của máy chủ EC2.
   * Nhấn **Create records**.
   * Tiếp tục tạo bản ghi A cho tên miền `www`: Click **Create record** -> Nhập **Record name** là `www` -> Chọn **Record type** là `A` -> Nhập cùng địa chỉ Elastic IP của EC2 vào ô **Value** -> Click **Create records**.

   ![Cấu hình bản ghi A và Name Servers](/images/5-Workshop/5.5-Policy/5.5.1_2.png)

3. **Cài đặt và cấp chứng chỉ SSL bằng Certbot Let's Encrypt:**
   * Trên terminal EC2, tắt tạm thời container Nginx (vì Certbot cần sử dụng cổng 80 để xác thực tên miền):
     ```bash
     docker stop cfe_di_rom_nginx
     ```
   * Cài đặt công cụ Certbot và tiến hành yêu cầu cấp chứng chỉ SSL cho tên miền của bạn:
     ```bash
     # Cập nhật và cài đặt Certbot
     sudo apt update
     sudo apt install certbot -y

     # Chạy Certbot chế độ độc lập (standalone) để xin cấp chứng chỉ cho cả tên miền gốc và www
     sudo certbot certonly --standalone -d jenkam.site -d www.jenkam.site
     ```
     *Lưu ý:* Chứng chỉ SSL sau khi cấp thành công sẽ được lưu trữ tại thư mục `/etc/letsencrypt/live/jenkam.site/`.



---

#### 2. Cấu hình Nginx chạy HTTPS (Cổng 443)
Sau khi có chứng chỉ SSL, chúng ta nâng cấp file cấu hình Nginx để tự động chuyển hướng mọi yêu cầu HTTP (cổng 80) sang HTTPS (cổng 443) bảo mật.

1. Chỉnh sửa tệp cấu hình Nginx trên EC2:
   `nano ~/cafe-app/nginx/conf.d/default.conf`
2. Thay thế toàn bộ nội dung bằng cấu hình SSL sau:
   ```nginx
   server {
       listen 80;
       server_name jenkam.site www.jenkam.site;
       return 301 https://$host$request_uri; # Chuyển hướng HTTP sang HTTPS bảo mật
   }

   server {
       listen 443 ssl;
       server_name jenkam.site www.jenkam.site;

       # Đường dẫn chứng chỉ SSL Let's Encrypt (được mount từ EC2 vào container)
       ssl_certificate /etc/letsencrypt/live/jenkam.site/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/jenkam.site/privkey.pem;

       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers HIGH:!aNULL:!MD5;

       # Điều hướng API Backend Spring Boot
       location /api/ {
           proxy_pass http://backend:8080/api/v1/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       # Điều hướng Next.js Frontend
       location / {
           proxy_pass http://frontend:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
3. Khởi chạy lại hệ thống container để Nginx áp dụng cấu hình mới:
   ```bash
   cd ~/cafe-app
   docker compose up -d
   ```
   *Bây giờ, bạn có thể truy cập hệ thống một cách an toàn qua địa chỉ: **`https://jenkam.site`**.*

---

#### 3. Thiết lập Cảnh báo lỗi tự động (AWS CloudWatch & SNS Alerts)
Trong tệp tin `docker-compose.yml`, dịch vụ backend đã được cấu hình đẩy trực tiếp logs hệ thống từ container lên CloudWatch Logs với tên group là `cfe-di-rom-logs`. Bây giờ chúng ta sẽ cấu hình để gửi email cảnh báo ngay lập tức cho lập trình viên mỗi khi hệ thống phát sinh lỗi.

##### Bước 3.1: Tạo SNS Topic để gửi thông báo email
1. Truy cập **Amazon SNS Console** -> Chọn **Topics** -> Click **Create topic**.
2. Chọn loại **Standard**, điền tên là `cfe-di-rom-alerts`. Click **Create topic**.
3. Click chọn Topic vừa tạo -> Bấm **Create subscription**.
4. Cấu hình Subscription:
   *   **Protocol**: Chọn **Email**.
   *   **Endpoint**: Nhập địa chỉ email cá nhân của bạn để nhận cảnh báo.
5. Click **Create subscription**.
6. **Xác nhận Subscription:** Mở hòm thư email của bạn, tìm thư có tiêu đề *AWS Notification - Subscription Confirmation* và nhấp chọn link **Confirm Subscription** để hoàn tất xác minh.

   ![Cấu hình SNS Topic](/images/5-Workshop/5.5-Policy/5.5.3_buoc3.1.png)

##### Bước 3.2: Thiết lập Metric Filter trên CloudWatch Logs
1. Truy cập **CloudWatch Console** -> Chọn **Log groups** ở menu bên trái -> Nhấp chọn log group **`cfe-di-rom-logs`**.
2. Chọn tab **Metric filters** -> Click **Create metric filter**.
3. Cấu hình Filter:
   *   **Filter pattern**: Nhập `?ERROR ?Exception` (Bộ lọc tìm kiếm các dòng log chứa từ khóa ERROR hoặc Exception).
   *   **Metric name**: `BackendErrorCount`
4. Bấm **Save metric filter**.

   ![Cấu hình Metric Filter](/images/5-Workshop/5.5-Policy/5.5.3_buoc3.2.png)

##### Bước 3.3: Khởi tạo CloudWatch Alarm
1. Nhấp chọn Metric filter `BackendErrorCount` vừa tạo -> Click **Create alarm**.
2. Cấu hình điều kiện Alarm:
   *   **Statistic**: Chọn `Sum`.
   *   **Period**: Chọn `1 minute`.
   *   **Whenever BackendErrorCount is...**: Chọn `Greater than or equal to 1` (Báo động khi có từ 1 lỗi trở lên xuất hiện trong 1 phút).
3. Cấu hình hành động (Actions):
   *   Mục **Notification**, chọn trạng thái kích hoạt **In alarm**.
   *   Chọn gửi thông báo tới SNS Topic **`cfe-di-rom-alerts`** đã tạo ở Bước 3.1.
4. Đặt tên Alarm là `Backend-Logic-Error-Alarm` -> Bấm **Create alarm**.
   *Từ nay, mỗi khi backend Spring Boot xảy ra lỗi logic hoặc lỗi tràn bộ nhớ (OOM) làm phát sinh log ERROR, hệ thống AWS sẽ tự động gửi email cảnh báo trực tiếp về hòm thư của bạn.*

   ![Cấu hình CloudWatch Alarm](/images/5-Workshop/5.5-Policy/5.5.3_buoc3.3.png)


---
title : "Khởi tạo EC2 và Thiết lập môi trường"
date : 2024-01-01 
weight : 3
chapter : false
pre : " <b> 5.3. </b> "
---

Trong phần này, chúng ta sẽ tiến hành khởi tạo máy chủ ảo Amazon EC2 trên vùng **Sydney (ap-southeast-2)**, cấu hình bộ nhớ ảo Swap File 2GB và cài đặt môi trường chạy Docker để chuẩn bị triển khai WEB_JENIKA.

---

#### 1. Khởi tạo máy chủ EC2 và Gán Elastic IP
Để chạy các dịch vụ web, chúng ta cần tạo một máy chủ ảo Ubuntu Server:

##### Các bước khởi tạo EC2 Instance:
1. Đăng nhập vào AWS Console, chọn vùng **Sydney**.
2. Tìm kiếm dịch vụ **EC2** -> Chọn **Instances** ở thanh bên trái -> Click **Launch instances**.
3. Cấu hình máy chủ:
   *   **Name**: `cafe-app-server`
   *   **Application and OS Images (AMI)**: Chọn **Ubuntu** (Ubuntu Server 22.04 LTS, 64-bit x86).
   *   **Instance type**: Chọn **`t3.micro`** (hoặc `t2.micro` tùy vùng được Free Tier hỗ trợ).
   *   **Key pair (login)**: Chọn khóa `.pem` sẵn có của bạn hoặc tạo khóa mới để tải về (ví dụ: `dashboard_manage_coffe.pem`) phục vụ kết nối SSH.
   *   **Network settings**:
       *   Chọn **Select existing security group** và tích chọn nhóm bảo mật **`web-app-sg`** đã tạo ở Mục 5.2.
   *   **Advanced details**:
       *   **IAM instance profile**: Chọn **`WebJenika-EC2-InstanceProfile`** (đã được tạo tự động thông qua IAM Role `WebJenika-EC2-Role` ở Mục 5.2 để tự động cấp quyền ghi S3 và CloudWatch cho máy chủ).
4. Nhấn **Launch instance** và đợi khoảng 1 phút để máy chủ khởi chạy.

   ![Khởi tạo EC2 và Gán Elastic IP](/images/5-Workshop/5.3-S3-vpc/5.3.1.2.png)

##### Cấp phát và gán Elastic IP (IP tĩnh):
Mặc định khi máy chủ EC2 tắt đi bật lại, IP công cộng sẽ thay đổi, làm mất liên kết với tên miền DDNS. Vì vậy ta cần cấp Elastic IP cố định:
1. Tại EC2 Console, chọn mục **Elastic IPs** ở menu bên trái -> Click **Allocate Elastic IP address**.
2. Chọn **Allocate** để tạo IP tĩnh mới.
3. Tích chọn IP vừa tạo -> Bấm **Actions** -> Chọn **Associate Elastic IP address**.
4. Tại ô **Instance**, chọn máy chủ `cafe-app-server` mới tạo. Nhấn **Associate** để hoàn tất liên kết IP tĩnh.



---

#### 2. Thiết lập Swap File 2GB (Bộ nhớ RAM ảo)
Máy chủ EC2 Free Tier (`t3.micro`) chỉ có **1 GB RAM vật lý**. Khi chạy đồng thời cả MySQL Database, Spring Boot Backend và Next.js Frontend, hệ thống sẽ rất dễ bị quá tải bộ nhớ và gặp lỗi **Out Of Memory (OOM)** dẫn đến việc database bị ngắt đột ngột. Để giải quyết, chúng ta cấu hình thêm **2 GB Swap File** làm RAM ảo trên ổ đĩa SSD.

1. Sử dụng terminal trên máy cá nhân để kết nối SSH tới EC2 (thay thế địa chỉ IP bằng Elastic IP của bạn):
   ```bash
   ssh -i "dashboard_manage_coffe.pem" ubuntu@your-ec2-elastic-ip
   ```
2. Thực thi tuần tự các câu lệnh sau để tạo và kích hoạt Swap File:
   ```bash
   # 1. Tạo file swap trống dung lượng 2GB
   sudo fallocate -l 2G /swapfile

   # 2. Phân quyền chỉ cho root đọc/ghi file swap vì lý do bảo mật
   sudo chmod 600 /swapfile

   # 3. Định dạng file thành không gian Swap
   sudo mkswap /swapfile

   # 4. Kích hoạt sử dụng swapfile trong hệ thống
   sudo swapon /swapfile

   # 5. Ghi cấu hình vào fstab để swap tự động kích hoạt mỗi khi EC2 khởi động lại
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```
3. Kiểm tra lại dung lượng bộ nhớ để xác nhận Swap đã hoạt động thành công:
   ```bash
   free -h
   ```
   *Kết quả thực tế hiển thị từ máy chủ EC2 của bạn khi hệ thống đang hoạt động:*
   ```text
   ubuntu@ip-172-31-10-185:~/cafe-app$ free -h
                  total        used        free      shared  buff/cache   available
   Mem:           908Mi       624Mi        74Mi       2.1Mi       324Mi       284Mi
   Swap:          2.0Gi       678Mi       1.3Gi
   ```
   *Nhận xét thực tế:* Máy chủ hiện đang tiêu tốn `624Mi` bộ nhớ RAM vật lý cho hệ điều hành cùng các container Docker, đồng thời hệ thống tự động đẩy thêm `678Mi` dữ liệu sang bộ nhớ ảo **Swap (RAM ảo)**. Nếu không cấu hình Swap File 2GB này, máy chủ EC2 Free Tier (chỉ có 1GB RAM vật lý) chắc chắn sẽ bị quá tải bộ nhớ và sập hoàn toàn tiến trình MySQL Database/Spring Boot lập tức (lỗi Out Of Memory - OOM).


---

#### 3. Cài đặt Docker & Docker Compose
Docker giúp đóng gói và chạy các dịch vụ Next.js, Spring Boot, MySQL, Nginx độc lập và nhất quán trên máy chủ EC2.

1. Cập nhật hệ thống và cài đặt Docker:
   ```bash
   # Cập nhật danh sách gói phần mềm
   sudo apt update && sudo apt upgrade -y

   # Cài đặt Docker và Docker Compose V2
   sudo apt install docker.io docker-compose-v2 -y
   ```
2. Thêm người dùng hiện tại (`ubuntu`) vào nhóm `docker` để chạy các lệnh docker trực tiếp mà không cần tiền tố `sudo`:
   ```bash
   sudo usermod -aG docker $USER
   
   # Áp dụng quyền hạn mới cho phiên đăng nhập hiện tại
   newgrp docker
   ```
   *Kiểm tra danh sách nhóm của user `ubuntu` để xác nhận đã thuộc nhóm `docker`:*
   ```bash
   groups
   ```
   *Kết quả thực tế hiển thị trên máy chủ:*
   ```text
   ubuntu@ip-172-31-10-185:~/cafe-app$ groups
   ubuntu adm cdrom sudo dip plugdev lxd default-ec2-users docker
   ```

3. Xác nhận cài đặt thành công bằng cách kiểm tra phiên bản:
   ```bash
   docker --version
   docker compose version
   ```
   *Kết quả thực tế hiển thị trên máy chủ EC2 của bạn:*
   ```text
   ubuntu@ip-172-31-10-185:~/cafe-app$ docker --version
   Docker version 29.1.3, build 29.1.3-0ubuntu4.1

   ubuntu@ip-172-31-10-185:~/cafe-app$ docker compose version
   Docker Compose version v2.29.1
   ```
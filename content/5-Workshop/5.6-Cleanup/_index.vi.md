---
title : "Dọn dẹp tài nguyên"
date : 2024-01-01 
weight : 6
chapter : false
pre : " <b> 5.6. </b> "
---

Sau khi hoàn thành bài thực hành hoặc khi kết thúc kỳ thực tập, việc dọn dẹp và xóa các tài nguyên đã tạo trên đám mây AWS là cực kỳ quan trọng để tránh phát sinh chi phí ngoài ý muốn (đặc biệt khi tài khoản của bạn hết hạn gói Free Tier).

---

#### Quy trình dọn dẹp tài nguyên từng bước:

##### Bước 1: Xóa máy chủ ảo EC2 (Terminate Instance)
1. Đăng nhập vào AWS Management Console, chọn vùng **Sydney (`ap-southeast-2`)**.
2. Truy cập **EC2 Console** -> Chọn mục **Instances** -> Tìm kiếm máy chủ `cafe-app-server`.
3. Tích chọn máy chủ -> Click **Instance state** -> Chọn **Terminate instance** (Xóa vĩnh viễn máy chủ).
4. Nhấn **Terminate** để xác nhận. Sau khi máy chủ bị xóa, các Docker container và dữ liệu không lưu trong volume độc lập sẽ bị hủy hoàn toàn.

##### Bước 2: Giải phóng Elastic IP (Release Elastic IP)
*Lưu ý:* AWS tính phí cho các địa chỉ Elastic IP đã cấp phát nhưng không được liên kết với bất kỳ máy chủ đang chạy nào.
1. Tại EC2 Console, chọn mục **Elastic IPs** ở menu bên trái.
2. Tích chọn địa chỉ IP tĩnh đã cấp phát cho máy chủ trước đó.
3. Click vào nút **Actions** ở góc trên -> Chọn **Release Elastic IP addresses**.
4. Xác nhận **Release** để hoàn trả lại địa chỉ IP cho AWS.

##### Bước 3: Xóa Amazon S3 Bucket (`jenkam-images`)
AWS không cho phép xóa trực tiếp một S3 bucket khi bên trong vẫn còn dữ liệu. Vì vậy bạn phải làm trống trước:
1. Truy cập **S3 Console** -> Chọn bucket **`jenkam-images`** (hoặc bucket bạn đã tạo).
2. Click chọn nút **Empty** ở trên thanh menu.
3. Nhập cụm từ `permanently delete` vào ô xác nhận để xóa toàn bộ các tệp tin hình ảnh trong thư mục `invoices/` và `temp/` -> Click **Empty**.
4. Quay trở lại màn hình S3 Buckets -> Tích chọn bucket đó một lần nữa -> Click nút **Delete**.
5. Nhập chính xác tên bucket để xác nhận và click **Delete bucket** để xóa hoàn toàn.

##### Bước 4: Xóa IAM Role và Security Group
1. **Xóa IAM Role:** 
   * Truy cập **IAM Console** -> Chọn **Roles** ở cột bên trái.
   * Tìm kiếm và tích chọn Role **`WebJenika-EC2-Role`** -> Click nút **Delete**.
   * Nhập tên Role để xác nhận xóa.
2. **Xóa Security Group:**
   * Truy cập **EC2 Console** -> Chọn **Security Groups** ở cột bên trái.
   * Tích chọn nhóm bảo mật **`web-app-sg`** -> Click **Actions** -> Chọn **Delete security group**.
   * Xác nhận xóa.

##### Bước 5: Xóa CloudWatch Log Group và SNS Topic
1. **Xóa Logs:** 
   * Truy cập **CloudWatch Console** -> Chọn **Log groups** -> Tích chọn **`cfe-di-rom-logs`**.
   * Click **Actions** -> Chọn **Delete log group(s)** và xác nhận.
2. **Xóa SNS Topic:**
   * Truy cập **SNS Console** -> Chọn **Topics** -> Tích chọn **`cfe-di-rom-alerts`**.
   * Click **Delete** và nhập cụm từ xác nhận để xóa hoàn toàn (các Subscription email đi kèm sẽ tự động bị hủy).
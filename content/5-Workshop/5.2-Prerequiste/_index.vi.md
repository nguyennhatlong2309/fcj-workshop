---
title : "Các bước chuẩn bị"
date : 2024-01-01 
weight : 2
chapter : false
pre : " <b> 5.2. </b> "
---

#### 1. Chuẩn bị môi trường Local (Local Prerequisites)
Để phục vụ việc build, đóng gói ứng dụng thành các Docker image và kết nối đến tài nguyên đám mây, máy tính cá nhân của bạn cần chuẩn bị sẵn các công cụ sau:
*   **Java Development Kit (JDK) 17**: Phiên bản JDK yêu cầu để chạy ứng dụng máy tính và backend.
*   **Apache Maven**: Dùng để quản lý thư viện và biên dịch dự án Java/Spring Boot.
*   **Node.js (v18+)**: Để cài đặt thư viện và khởi chạy Frontend Next.js.
*   **Git & SSH Client**: Phục vụ việc clone mã nguồn và kết nối SSH bảo mật vào máy chủ EC2.
*   **Docker & Docker Desktop**: Dùng để build các Docker image (`helios2309/cafe-backend:latest`, `helios2309/cafe-frontend:latest`) ở local và push lên Docker Hub trước khi kéo về triển khai trên EC2.
*   **Tài khoản Docker Hub**: Dùng để lưu trữ các Docker image của dự án (ví dụ tài khoản: `helios2309`).

---

#### 2. Quyền hạn IAM (IAM Permissions)
Đảm bảo tài khoản AWS IAM User của bạn có đủ quyền hạn để tạo lập và dọn dẹp các tài nguyên trong workshop này. Hãy gắn policy sau vào tài khoản của bạn:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "WebJenikaWorkshopPermissions",
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

#### 3. Khởi tạo tài nguyên hạ tầng bằng AWS Console
Vì toàn bộ hệ thống (Next.js Frontend, Spring Boot Backend, MySQL Database và Nginx) được triển khai chung trên một máy chủ ảo EC2 duy nhất bằng Docker Compose, chúng ta sẽ tận dụng **Mạng VPC mặc định (Default VPC)** có sẵn của tài khoản AWS và tạo thủ công các tài nguyên bổ trợ sau:

##### 3.1. Khởi tạo Security Group cho EC2 (`web-app-sg`)
Để cho phép truy cập web và SSH kết nối từ xa:
1. Đăng nhập vào AWS Management Console, chuyển vùng sang **Sydney (`ap-southeast-2`)**.

   ![Cấu hình Security Group](/images/5-Workshop/5.2-Prerequisite/5.2_3.1.1.png)

2. Tìm kiếm dịch vụ **EC2** -> Chọn **Security Groups** ở thanh bên trái -> Click **Create security group**.
3. Cấu hình thông tin cơ bản:
   * **Security group name**: `web-app-sg`
   * **Description**: `Allow SSH, HTTP, and HTTPS access to EC2`
   * **VPC**: Chọn **VPC mặc định (Default VPC)** của phân vùng Sydney.
4. Tại mục **Inbound rules** (Quy tắc đầu vào), thêm 3 quy tắc sau:
   * **Quy tắc 1**: Type `SSH` (Cổng 22) -> Source: Chọn `My IP` (hoặc `Anywhere-IPv4` - `0.0.0.0/0` để kết nối từ bất kỳ mạng nào).
   * **Quy tắc 2**: Type `HTTP` (Cổng 80) -> Source: Chọn `Anywhere-IPv4` (`0.0.0.0/0`).
   * **Quy tắc 3**: Type `HTTPS` (Cổng 443) -> Source: Chọn `Anywhere-IPv4` (`0.0.0.0/0`).
5. Cuộn xuống và click **Create security group**. Ghi lại ID của Security Group mới tạo (ví dụ: `sg-0123456789abcdef0`).

   ![Cấu hình Quy tắc đầu vào](/images/5-Workshop/5.2-Prerequisite/5.2_3.1.234.png)


##### 3.2. Khởi tạo Amazon S3 Bucket (`jenkam-images`)
Để lưu trữ các tệp tin hình ảnh hóa đơn phục vụ tính năng OCR:
1. Tìm kiếm và chọn dịch vụ **S3** trên AWS Console -> Click **Create bucket**.
2. Thiết lập thông tin:
   * **Bucket name**: Đặt tên duy nhất toàn cầu (ví dụ: `jenkam-images`).
   * **AWS Region**: Chọn **ap-southeast-2** (Sydney) để cùng vùng với máy chủ EC2.
3. Phần **Block Public Access settings for this bucket**: Giữ tùy chọn mặc định **Block all public access** để bảo mật dữ liệu nội bộ.
4. Cuộn xuống cuối trang và click **Create bucket**.
5. **Khởi tạo cấu trúc thư mục (Folders):**
   * Truy cập vào bucket `jenkam-images` vừa tạo -> Click **Create folder**.
   * Tạo thư mục thứ nhất: Tên là `invoices` (để lưu trữ ảnh hóa đơn lâu dài). Click **Create folder**.
   * Tạo thư mục thứ hai: Tên là `temp` (để lưu trữ các tệp tạm thời trong quá trình xử lý OCR). Click **Create folder**.

   ![Cấu hình Thư mục S3](/images/5-Workshop/5.2-Prerequisite/5.2_3.2.12345.png)

6. **Cấu hình Quy tắc vòng đời (Lifecycle Rule) cho thư mục `temp`:**
   Để tự động dọn dẹp các tệp ảnh tạm thời nhằm tối ưu dung lượng và chi phí:
   * Chuyển sang tab **Management** của bucket -> Tại mục **Lifecycle rules**, click **Create lifecycle rule**.
   * Cấu hình quy tắc:
     * **Lifecycle rule name**: `CleanTempFolder`
     * **Rule scope**: Chọn **Limit the scope of this rule using one or more filters**.
     * **Prefix**: Nhập `temp/` (lưu ý có dấu gạch chéo `/` ở cuối để áp dụng riêng cho các đối tượng trong thư mục `temp`).
     * **Lifecycle rule actions**: Tích chọn **Expire current versions of objects**.
     * **Expire current versions of objects**: Tại ô **Days after object creation**, điền `1` ngày (hệ thống sẽ tự động xóa các file tạm trong thư mục `temp` sau 24 giờ kể từ khi tải lên).
   * Click **Create rule** để hoàn tất.

   ![Cấu hình Quy tắc vòng đời S3](/images/5-Workshop/5.2-Prerequisite/5.2_3.2.6.png)



##### 3.3. Khởi tạo IAM Role cho EC2 (`WebJenika-EC2-Role`)
Cấp quyền bảo mật để EC2 giao tiếp với S3 và đẩy log Docker trực tiếp lên CloudWatch Logs:
1. Tìm kiếm dịch vụ **IAM** trên AWS Console -> Chọn **Roles** ở thanh bên trái -> Click **Create role**.
2. Chọn loại thực thể tin cậy (**Trusted entity type**): **AWS service** -> Chọn case sử dụng (**Use case**): **EC2**. Click **Next**.
3. Tại phần **Add permissions** (Thêm quyền hạn), tìm kiếm và tích chọn hai chính sách bảo mật sau:
   * `AmazonS3FullAccess` (hoặc tạo Custom Policy chỉ cho phép thao tác trên bucket `jenkam-images`).
   * `CloudWatchLogsFullAccess` (cho phép đẩy logs của Docker backend lên CloudWatch).
4. Nhấn **Next**. Thiết lập thông tin định danh:
   * **Role name**: `WebJenika-EC2-Role`
5. Nhấn **Create role** để hoàn thành. Hệ thống sẽ tự động tạo một **Instance Profile** cùng tên để bạn gán vào máy chủ EC2 khi khởi tạo.

   ![Cấu hình IAM Role cho EC2](/images/5-Workshop/5.2-Prerequisite/5.2_3.3.png)

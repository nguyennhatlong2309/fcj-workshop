---
title: "Workshop"
date: 2024-01-01
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

# Triển khai hệ thống JENKAM trên đám mây AWS

#### Tổng quan

Trong workshop này, chúng ta sẽ học cách triển khai thực tế hệ thống quản lý quán cà phê **JENKAM (CAFE_DI_ROM)** lên nền tảng đám mây **Amazon Web Services (AWS)**. Đây là một bài thực hành hướng dẫn quy trình đóng gói ứng dụng bằng Docker và chạy trên một máy chủ ảo EC2 duy nhất (sử dụng mạng Default VPC của AWS để tối ưu chi phí trong gói Free Tier). 

Hệ thống được thiết kế theo các tiêu chuẩn vận hành thực tế bao gồm:
*   **Reverse Proxy & SSL**: Sử dụng Nginx làm reverse proxy và Certbot Let's Encrypt cấp chứng chỉ bảo mật cho tên miền (`jenkam.site`).
*   **Bảo mật IAM**: Sử dụng IAM Instance Profile gắn quyền cho EC2 thay vì lưu trữ cứng credentials.
*   **Lưu trữ đám mây**: Tích hợp Amazon S3 để lưu trữ dữ liệu hình ảnh hóa đơn cho tính năng OCR.
*   **Giám sát & Cảnh báo**: Đẩy log container trực tiếp từ Docker lên AWS CloudWatch Logs và cấu hình AWS SNS gửi cảnh báo email tự động khi backend phát sinh lỗi hệ thống.

#### Liên kết tham khảo
*   **Resource (GitHub)**: [https://github.com/nguyennhatlong2309/APP_JENIKA.git](https://github.com/nguyennhatlong2309/APP_JENIKA.git)
*   **Production**: [https://jenkam.site](https://jenkam.site)

#### Nội dung bài thực hành

1. [Tổng quan về workshop](5.1-workshop-overview/)
2. [Các bước chuẩn bị](5.2-prerequiste/)
3. [Khởi tạo EC2 và thiết lập môi trường](5.3-s3-vpc/)
4. [Triển khai Docker Compose & Cơ sở dữ liệu](5.4-s3-onprem/)
5. [Cấu hình Tên miền, SSL & Cảnh báo lỗi tự động](5.5-policy/)
6. [Dọn dẹp tài nguyên](5.6-cleanup/)

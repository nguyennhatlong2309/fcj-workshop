---
title : "Giới thiệu"
date : 2024-01-01 
weight : 1
chapter : false
pre : " <b> 5.1. </b> "
---

#### Nền tảng Web WEB_JENIKA
+ **WEB_JENIKA (WEB_CAFE)** là hệ thống quản lý quán cà phê, kho hàng và doanh thu toàn diện trên nền tảng web. Hệ thống này hoạt động song song và đồng bộ dữ liệu với **BrewMaster Pro (Java Swing Desktop App)** thông qua việc chia sẻ một cơ sở dữ liệu MySQL chung.
+ Ứng dụng sở hữu giao diện Next.js (React 19) hiện đại với phong cách **Glassmorphism** sang trọng, kết hợp cùng hệ thống REST API mạnh mẽ xây dựng trên **Spring Boot 3.3**.

#### Tổng quan và Kiến trúc Workshop
Trong workshop này, bạn sẽ tiến hành triển khai ứng dụng WEB_JENIKA trên đám mây AWS với một kiến trúc tối ưu chi phí (Free Tier), bảo mật và dễ dàng mở rộng:
+ **Amazon EC2**: Đóng vai trò là máy chủ ứng dụng để chạy toàn bộ các container Docker (Nginx Reverse Proxy, Next.js Frontend, Spring Boot Backend, cơ sở dữ liệu MySQL và Hermes Agent) trong cùng một mạng ảo nội bộ. Để tránh lỗi tràn bộ nhớ (OOM) do hạn chế của gói Free Tier, một tệp Swap File 2GB sẽ được thiết lập trên EC2.
+ **MySQL Database**: Cơ sở dữ liệu được chạy trực tiếp dưới dạng container trên EC2 và cấu hình Docker Volume để ghi dữ liệu lâu bền.
+ **Amazon S3**: Lưu trữ các tệp ảnh hóa đơn gốc và kết quả từ tính năng OCR hóa đơn một cách độc lập và lâu bền.
+ **AWS CloudWatch & SNS**: Sử dụng log driver `awslogs` của Docker để đẩy trực tiếp nhật ký hoạt động từ container Spring Boot lên CloudWatch Logs và cấu hình SNS gửi email cảnh báo tự động khi phát sinh lỗi `ERROR`.

![overview](/images/5-Workshop/5.1-Workshop-overview/graph.jpeg)

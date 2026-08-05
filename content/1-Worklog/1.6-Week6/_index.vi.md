---
title: "Worklog Tuần 6"
date: 2024-01-01
weight: 1
chapter: false
pre: " <b> 1.6. </b> "
---

### Mục tiêu tuần 6:

* Đóng gói Docker các thành phần (Next.js, Spring Boot, MySQL, Hermes Agent, Nginx).
* Khởi tạo máy chủ AWS EC2, cấu hình Swap File 2GB và cài đặt Docker/Docker Compose.

### Các công việc cần triển khai trong tuần này:
| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
| --- | --- | --- | --- | --- |
| Thứ Hai | - Viết Dockerfile cho Frontend, Backend, Hermes Agent và cấu hình tệp tin `docker-compose.yml`. | 13/07/2026 | 13/07/2026 | <https://cloudjourney.awsstudygroup.com/> |
| Thứ Ba | - Tạo máy chủ ảo AWS EC2 (t3.micro), gán Elastic IP và liên kết IAM Role (`EC2-Cafe-App-Role`). | 14/07/2026 | 14/07/2026 | <https://cloudjourney.awsstudygroup.com/> |
| Thứ Tư | - SSH vào máy chủ EC2, thiết lập Swap File 2GB (RAM ảo) để chuẩn bị RAM chạy hệ thống và cài đặt Docker. | 15/07/2026 | 15/07/2026 | <https://cloudjourney.awsstudygroup.com/> |
| Thứ Năm | - Nghiên cứu tài liệu cấu hình log driver và thiết lập Docker daemon trên môi trường EC2. | 16/07/2026 | 16/07/2026 | <https://cloudjourney.awsstudygroup.com/> |
| Thứ Sáu | - Chạy thử nghiệm Docker Compose các container trên máy chủ EC2, kiểm tra kết nối các container. | 17/07/2026 | 17/07/2026 | |

### Kết quả đạt được tuần 6:

* Đóng gói container Docker thành công cho toàn bộ hệ thống (Frontend, Backend, Hermes, MySQL, Nginx).
* Khởi tạo và thiết lập thành công máy chủ EC2 Free Tier kèm Swap File 2GB và Docker/Docker Compose.
* Đạt tổng cộng 3 buổi lên văn phòng và 2 buổi tham gia hoạt động trực tiếp (Event 1 & 2) (tích lũy từ tuần trước).

---
title: "Worklog Tuần 7"
date: 2024-01-01
weight: 1
chapter: false
pre: " <b> 1.7. </b> "
---

### Mục tiêu tuần 7:

* Cấu hình SSL Nginx, import database và kiểm thử tích hợp hệ thống trên môi trường AWS.
* Thiết lập CloudWatch Logs và cảnh báo lỗi tự động qua AWS SNS.
* Lên văn phòng làm việc trực tiếp (Buổi 6 & 7).

### Các công việc cần triển khai trong tuần này:
| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
| --- | --- | --- | --- | --- |
| Thứ Hai | - Xin cấp chứng chỉ SSL Let's Encrypt bằng Certbot ở chế độ standalone trên máy chủ EC2. | 20/07/2026 | 20/07/2026 | |
| Thứ Ba | - Cấu hình Nginx Reverse Proxy (HTTPS) trỏ về các container ứng dụng. | 21/07/2026 | 21/07/2026 | |
| Thứ Tư | - Import dữ liệu cơ sở dữ liệu ban đầu (`import_data.sql`) vào container MySQL trên EC2; Lên văn phòng làm việc. | 22/07/2026 | 22/07/2026 | |
| Thứ Năm | - Tạo SNS Topic, Subscribe Email và thiết lập CloudWatch Metric Filter quét log `ERROR`; Lên văn phòng làm việc. | 23/07/2026 | 23/07/2026 | <https://cloudjourney.awsstudygroup.com/> |
| Thứ Sáu | - Chạy thử nghiệm toàn diện các container trên EC2 và kiểm tra log đẩy lên CloudWatch. | 24/07/2026 | 24/07/2026 | |

### Kết quả đạt được tuần 7:

* Cấu hình thành công SSL Let's Encrypt và Nginx HTTPS cho ứng dụng.
* Import database và kiểm thử tích hợp hệ thống thành công trên môi trường đám mây AWS.
* Thiết lập thành công hệ thống giám sát log tự động qua CloudWatch Logs và cảnh báo email qua SNS.
* Đạt tổng cộng 5 buổi lên văn phòng và 2 buổi tham gia hoạt động trực tiếp (Event 1 & 2) (tích lũy từ tuần trước).

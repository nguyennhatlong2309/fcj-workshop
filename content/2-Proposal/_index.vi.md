---
title: "Bản đề xuất"
date: 2024-01-01
weight: 2
chapter: false
pre: " <b> 2. </b> "
---
# BrewMaster Pro & JENKAM (WEB_CAFE)  
## Hệ thống quản lý toàn diện quán cà phê đa nền tảng (Desktop & Web App) tích hợp AWS Cloud  

### 1. Tóm tắt điều hành  
Dự án **BrewMaster Pro & JENKAM** được thiết kế nhằm cung cấp giải pháp quản lý quán cà phê, kho hàng, đối tác, nhân viên và doanh thu toàn diện. Hệ thống tích hợp song song cả ứng dụng Desktop (**Java Swing**) dành cho vận hành tại quầy và ứng dụng Web (**Next.js / React 19** kết hợp **Spring Boot**) dành cho quản trị viên và truy cập từ xa. Hệ thống chia sẻ một cơ sở dữ liệu MySQL tập trung và tận dụng hạ tầng dịch vụ điện toán đám mây **Amazon Web Services (AWS)** (bao gồm EC2, S3, CloudWatch, SNS) kết hợp tên miền riêng `jenkam.site` (đăng ký tại Nhân Hòa) và quản lý định tuyến DNS qua **AWS Route 53** để đảm bảo tính sẵn sàng cao, bảo mật và tối ưu hóa chi phí vận hành. Toàn bộ các dịch vụ (bao gồm cả cơ sở dữ liệu MySQL) được triển khai trên cùng một máy chủ ảo EC2 bằng Docker Compose.

Đặc biệt, để làm đa dạng và tăng tính hiện đại cho dự án, hệ thống đã tận dụng sức nóng của kho lưu trữ **Hermes Agent** (link GitHub: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent.git)) hiện đang đạt cột mốc ấn tượng với 226k stars. Hermes Agent có khả năng tự động tối ưu hóa, học hỏi và trở nên thông minh hơn theo thời gian sử dụng. Hệ thống tích hợp Hermes Agent bằng cách sử dụng các mô hình ngôn ngữ lớn (LLMs) miễn phí thông qua cổng **OpenRouter**, đồng thời thiết lập cho Hermes một Skill (kỹ năng hành động) đặc biệt. Kỹ năng này cho phép Hermes tự động tạo các đơn nhập hàng hoặc bán hàng bằng cách nhận diện và trích xuất dữ liệu từ hình ảnh hóa đơn do người dùng gửi qua các bot trò chuyện (như Telegram hoặc Discord) đã được cấu hình. Để thực hiện điều này một cách bảo mật, Hermes Agent được cấp một mã **JWT (JSON Web Token) đặc biệt** cho phép nó thực thi các yêu cầu ghi dữ liệu (POST requests) vào hệ thống Backend. Việc tích hợp tác nhân thông minh AI này không chỉ giúp tối ưu hóa quy trình nhập liệu thủ công truyền thống mà còn làm phong phú giải pháp kiến trúc của dự án, chứng minh khả năng kết hợp công nghệ AI Agent tiên tiến trong ứng dụng thực tiễn.

### 2. Tuyên bố vấn đề  
*Vấn đề hiện tại*  
Nhiều cửa hàng cà phê và chuỗi bán lẻ nhỏ hiện nay vẫn quản lý dữ liệu kinh doanh một cách thủ công thông qua các bảng tính **Excel**. Phương pháp này dẫn đến nhiều hạn chế nghiêm trọng:
+ **Sai sót dữ liệu**: Việc nhập liệu thủ công dễ dẫn đến sai sót, nhầm lẫn số lượng kho, đơn giá và tính toán doanh thu.
+ **Thiếu đồng bộ thời gian thực**: Dữ liệu kho hàng, bán hàng và thu chi không được cập nhật tức thời giữa các bộ phận hoặc giữa các chi nhánh khác nhau.
+ **Khó khăn trong đối soát**: Thiếu tính năng lưu trữ vết hoạt động (Activity Log) dẫn đến khó khăn khi đối soát doanh thu và phát hiện thất thoát.
+ **Rủi ro mất dữ liệu**: Các tệp Excel lưu cục bộ trên máy tính dễ bị hỏng, mất mát do virus hoặc lỗi phần cứng và không có cơ chế tự động sao lưu an toàn.
+ **Khó khăn khi mở rộng**: Excel không thể đáp ứng việc phân quyền nhân viên chi tiết, quản lý công nợ nhà cung cấp hay tự động nhận dạng hóa đơn nhập kho bằng công nghệ OCR.

*Giải pháp & Yêu cầu của người dùng*  
Để giải quyết triệt để các vấn đề trên, hệ thống được thiết kế với các chức năng và form dữ liệu chuyên biệt theo yêu cầu của người dùng:
1. **Bảng điều khiển (Dashboard)**: Trực quan hóa doanh thu, chi phí, lợi nhuận dưới dạng biểu đồ theo thời gian thực (ngày/tháng/năm).
2. **Form Quản lý bán hàng (Sales Orders)**: Lập hóa đơn bán lẻ nhanh chóng, tích hợp công cụ tìm kiếm sản phẩm và liên kết thông tin khách hàng thành viên.
3. **Form Quản lý nhập hàng (Purchase Orders)**: Quản lý chi tiết các đơn nhập nguyên vật liệu, thiết bị, theo dõi công nợ nhà cung cấp và lịch sử giao dịch.
4. **Form Quản lý kho (Inventory)**: Theo dõi số lượng tồn kho thực tế, tự động gửi cảnh báo thông minh khi hàng hóa dưới mức tối thiểu.
5. **Form Quản lý thu chi (Expenses)**: Ghi nhận chi phí vận hành quán (điện, nước, mặt bằng, lương nhân viên, v.v.).
6. **Form Quản lý đối tác (Partners)**: Lưu trữ và phân loại hồ sơ khách hàng thân thiết cùng các nhà cung cấp.
7. **Form Quản lý nhân viên & Phân quyền linh hoạt (Staff & Flexible Permissions)**: Quản lý hồ sơ nhân sự chi tiết và thiết lập hệ thống phân quyền linh hoạt theo từng vai trò (Quản trị viên, Quản lý, Nhân viên bán hàng, Nhân viên kho) để hạn chế hoặc mở rộng quyền truy cập các form nghiệp vụ và dữ liệu nhạy cảm.
8. **Tích hợp OCR Hóa đơn & AWS S3**: Tự động quét và lưu trữ ảnh hóa đơn gốc lên Amazon S3, trích xuất dữ liệu hóa đơn phục vụ nhập kho nhanh.
9. **Trang Quản lý hoạt động (Activity Log)**: Lưu trữ và rà soát toàn bộ lịch sử hoạt động, các thao tác nghiệp vụ đã thực hiện trước đó của tất cả người dùng trong hệ thống để phục vụ đối soát và tăng tính minh bạch dữ liệu.

### 3. Kiến trúc giải pháp  
Hệ thống được triển khai trên hạ tầng AWS chuẩn Production-ready:
+ **Tầng máy khách**: Người dùng truy cập Web App qua Trình duyệt web hoặc Desktop App Java Swing kết nối trực tiếp đến DB.
+ **Tầng ứng dụng & dữ liệu (Amazon EC2)**: Triển khai các container Docker bao gồm Nginx (Reverse Proxy & SSL), Next.js Frontend, Spring Boot Backend và cơ sở dữ liệu MySQL thông qua Docker Compose.
+ **Tầng lưu trữ (Amazon S3)**: Lưu trữ không giới hạn ảnh hóa đơn OCR.
+ **Tầng tối ưu hiệu năng**: Cấu hình bộ nhớ ảo (Swap File) 2GB trên máy chủ EC2 để giảm tải và ngăn ngừa lỗi tràn bộ nhớ (OOM) cho cơ sở dữ liệu MySQL khi chạy chung với các ứng dụng khác.
+ **Giám sát & Cảnh báo**: Đẩy logs từ Docker lên **AWS CloudWatch** thông qua log driver `awslogs` và kích hoạt gửi email cảnh báo qua **AWS SNS** khi phát sinh lỗi hệ thống.

![JENKAM Architecture](/images/5-Workshop/5.1-Workshop-overview/new_aws_system.png)

*Dịch vụ AWS sử dụng & Giải pháp mạng*  
- **Amazon EC2**: Chạy toàn bộ hệ thống container (Next.js, Spring Boot, MySQL, Nginx) trên một máy chủ ảo duy nhất (cấu hình `t3.micro`), kết hợp Swap File 2GB làm RAM ảo.
- **Amazon S3**: Lưu trữ các tệp ảnh hóa đơn gốc cho tính năng OCR.
- **DNS & Domain (Nhân Hòa & AWS Route 53)**: Sử dụng tên miền riêng `jenkam.site` đăng ký tại Nhân Hòa (49.000 VNĐ/năm), được định tuyến thông qua AWS Route 53 để phân giải tên miền về địa chỉ Elastic IP của EC2.
- **AWS CloudWatch**: Thu thập và lọc nhật ký lỗi của container Backend.
- **AWS SNS**: Gửi thông báo email/SMS cảnh báo lập trình viên khi có lỗi hệ thống.

### 4. Triển khai kỹ thuật  
*Các giai đoạn triển khai*  
Dự án được triển khai qua các giai đoạn chính:
1. **Giai đoạn 1 (Tuần 1 - Tuần 3)**: Khởi động dự án, nghiên cứu dịch vụ AWS, điều chỉnh kế hoạch, thiết kế cơ sở dữ liệu và khởi tạo khung dự án (boilerplate).
2. **Giai đoạn 2 (Tuần 4 - Tuần 5)**: Phát triển các tính năng nghiệp vụ cốt lõi (Spring Boot, Next.js) và tích hợp AWS SDK (S3, OCR).
3. **Giai đoạn 3 (Tuần 6 - Tuần 7)**: Đóng gói container Docker, triển khai thử nghiệm lên AWS EC2, cấu hình SSL Nginx, import dữ liệu và thiết lập giám sát CloudWatch + SNS.
4. **Giai đoạn 4 (Tuần 8 - Tuần 9)**: Chạy thử nghiệm thực tế (Demo), ghi nhận phản hồi người dùng, hoàn thiện giao diện báo cáo song ngữ trên Hugo và gửi Mentor phê duyệt.

### 5. Lộ trình & Mốc triển khai  
- **Tuần 1-3**: Làm quen công ty, tham gia Event 1, tự học dịch vụ AWS, điều chỉnh đề tài, thiết kế DB và thiết lập khung dự án local.
- **Tuần 4-5**: Phát triển API Spring Boot & giao diện Next.js, cấu hình AWS SDK để upload ảnh và tích hợp dịch vụ OCR hóa đơn nhập kho.
- **Tuần 6-7**: Đóng gói Docker Compose, tạo máy chủ EC2, cấu hình SSL Let's Encrypt Nginx, import CSDL và thiết lập giám sát lỗi tự động CloudWatch Logs & AWS SNS.
- **Tuần 8-9**: Chạy thử nghiệm bản Demo hệ thống, nhận phản hồi người dùng để sửa lỗi UI/UX, tổng hợp tài liệu viết báo cáo thực tập song ngữ hoàn chỉnh trên Hugo gửi Mentor phê duyệt.

### 6. Ước tính ngân sách  
Nhờ tối ưu hóa kiến trúc hạ tầng và tận dụng gói **AWS Free Tier (12 tháng đầu)**, chi phí vận hành hệ thống cực kỳ tiết kiệm được thống kê chi tiết trong bảng dưới đây:

| Dịch vụ / Tài nguyên | Gói áp dụng | Chi phí (12 tháng đầu) | Chi phí (Từ tháng 13) | Chi tiết / Hạn mức |
| --- | --- | --- | --- | --- |
| **Amazon EC2** | AWS Free Tier | 0.00 USD/tháng | ~5.00 USD/tháng | Cấu hình `t3.micro`, miễn phí 750 giờ/tháng. (Chạy toàn bộ Nginx, Next.js, Spring Boot, MySQL). |
| **Amazon S3** | AWS Free Tier | 0.00 USD/tháng | ~0.50 USD/tháng | Miễn phí 5GB dung lượng lưu trữ trong năm đầu. |
| **AWS CloudWatch & SNS** | AWS Free Tier | 0.00 USD/tháng | ~0.50 USD/tháng | Miễn phí 5GB Logs và 1.000.000 thông báo email/tháng. |
| **Tên miền & Route 53** | Custom Domain | ~0.66 USD/tháng | ~0.66 USD/tháng | Đăng ký tên miền `jenkam.site` tại Nhân Hòa (49.000 VNĐ/năm, tương đương ~0.16 USD/tháng) và phí Hosted Zone của AWS Route 53 (0.50 USD/tháng). |
| **Tổng cộng** | | **~0.66 USD/tháng** | **~6.66 USD/tháng** | **Tiết kiệm tối đa chi phí nhờ tối ưu hóa tài nguyên.** |

### 7. Đánh giá rủi ro  
*Ma trận rủi ro*  
- **Tràn bộ nhớ RAM trên EC2 (OOM)**: Ảnh hưởng cao, xác suất trung bình.  
- **Thất thoát dữ liệu**: Ảnh hưởng nghiêm trọng, xác suất thấp.  
- **Lỗi kết nối API/Hạ tầng**: Ảnh hưởng trung bình, xác suất trung bình.  

*Chiến lược giảm thiểu & Dự phòng*  
- **Tránh OOM**: Thiết lập cấu hình **Swap File 2GB** trên máy chủ EC2 để làm bộ nhớ ảo, giúp hỗ trợ dung lượng RAM vật lý 1GB khi chạy đồng thời MySQL, Spring Boot và Next.js.
- **Bảo mật dữ liệu**: Dữ liệu MySQL được lưu trữ lâu bền thông qua **Docker Volume** ánh xạ ra ổ đĩa của máy chủ EC2, đồng thời thiết lập quy trình sao lưu định kỳ (Database Backup Dump) lên Amazon S3 hoặc máy chủ bên ngoài.
- **Lỗi kết nối**: Thiết lập Nginx Reverse Proxy với cơ chế logging chi tiết và cấu hình CloudWatch + SNS để phát hiện lỗi ngay lập tức và gửi email cảnh báo cho lập trình viên.

### 8. Kết quả kỳ vọng  
- **Chuyển đổi số thành công**: Thay thế hoàn toàn quy trình ghi chép thủ công bằng Excel sang hệ thống quản lý cơ sở dữ liệu tập trung, tự động và chính xác.
- **Nâng cao hiệu suất vận hành**: Giảm thời gian xử lý đơn hàng, nhập hàng và tính toán doanh thu lên tới 70%.
- **Bảo mật và an toàn dữ liệu**: Dữ liệu kinh doanh và hóa đơn OCR được lưu trữ lâu bền trên dịch vụ đám mây AWS với cơ chế phân quyền bảo mật chặt chẽ.
# Báo Cáo Thực Hành: Lập trình Python với giao thức AMQP (RabbitMQ)

## Broker sử dụng
- **Phần mềm:** RabbitMQ
- **Host:** `localhost` (Chạy local trên máy cá nhân)
- **Cổng mặc định:** `5672`
- **Thư viện Python:** `pika` (`pip install pika`)

## Cách chạy từng chương trình & Kết quả đạt được

### Bài 1: Gửi và nhận message cơ bản
1. Mở terminal 1, chạy consumer để lắng nghe:
   `python consumer_bai1.py`
2. Mở terminal 2, chạy producer để gửi tin nhắn:
   `python producer_bai1.py`

**Kết quả:** Producer in ra thông báo đã gửi. Consumer bắt được message và in ra màn hình cùng với thời gian thực.

### Bài 2: Mô phỏng cảm biến IoT (Truyền tải JSON)
1. Mở terminal 1, chạy ứng dụng giám sát:
   `python monitor_consumer_bai2.py`
2. Mở terminal 2, chạy ứng dụng mô phỏng cảm biến:
   `python sensor_producer_bai2.py`

**Kết quả:** Producer sinh dữ liệu giả lập (nhiệt độ, độ ẩm) mỗi 3 giây và đóng gói bằng JSON. Consumer đọc luồng JSON này, in ra log và hiển thị dòng `CANH BAO:` nếu nhiệt độ > 35 hoặc độ ẩm < 40.

### Bài 3: Điều phối cảnh báo với Direct Exchange
1. Mở terminal 1, khởi động Warning Consumer:
   `python warning_consumer_bai3.py`
2. Mở terminal 2, khởi động Critical Consumer:
   `python critical_consumer_bai3.py`
3. Mở terminal 3, khởi động Producer để đẩy các mức log:
   `python alert_producer_bai3.py`

**Kết quả:** 
- Producer đẩy 4 message với các mức `info`, `warning`, `critical`, `warning`.
- `warning_consumer_bai3.py` chỉ bắt được 2 message có routing_key là `warning`.
- `critical_consumer_bai3.py` chỉ bắt được 1 message có routing_key là `critical`.
- Message `info` bị drop (hoặc không ai nhận) do không có queue nào bind với routing key này. Hệ thống đã phân luồng chính xác.

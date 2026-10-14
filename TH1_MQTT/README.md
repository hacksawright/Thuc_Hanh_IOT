# BÀI 1 - GIAO TIẾP MQTT CƠ BẢN

## 1. MQTT BROKER SỬ DỤNG

**Broker:** `test.mosquitto.org`  
**Port:** `1883`  
**Protocol:** MQTT

**Topic sử dụng:**

`iot/lab/message`

## 2. CÁC FILE CHƯƠNG TRÌNH

- `publisher_bai1.py`: Chương trình Publisher, gửi các message lên MQTT Broker.
- `subscriber_bai1.py`: Chương trình Subscriber, nhận và hiển thị các message từ MQTT Broker.

## 3. CÁCH CHẠY CHƯƠNG TRÌNH

**Bước 1: Mở Terminal 1 và chạy Subscriber:**

```bash
python subscriber_bai1.py
```

Subscriber sẽ kết nối tới MQTT Broker và đăng ký topic:
`iot/lab/message`

**Bước 2: Mở Terminal 2 và chạy Publisher:**

```bash
python publisher_bai1.py
```

Publisher sẽ kết nối tới MQTT Broker và gửi nhiều message liên tiếp.

## 4. KẾT QUẢ ĐẠT ĐƯỢC

- Kết nối thành công tới MQTT Broker `test.mosquitto.org`.
- Publisher gửi message đúng tới topic `iot/lab/message`.
- Mỗi message chứa thông tin của một thành viên trong nhóm.
- Publisher có thể gửi nhiều message liên tiếp.
- Subscriber nhận được các message từ Publisher và hiển thị:
  - Topic
  - Payload
  - Thời gian nhận message
- Subscriber tiếp tục chạy và lắng nghe message cho đến khi người dùng nhấn `Ctrl+C`.

---

# BÀI 2 - MÔ PHỎNG CẢM BIẾN NHIỆT ĐỘ VÀ ĐỘ ẨM BẰNG MQTT

## 1. MQTT BROKER SỬ DỤNG

**Broker:** `test.mosquitto.org`  
**Port:** `1883`  
**Protocol:** MQTT

**Các topic sử dụng:**

- `iot/lab/sensor01/data`
- `iot/lab/sensor02/data`

## 2. CÁC FILE CHƯƠNG TRÌNH

- `sensor_publisher_bai2.py`:  
  Mô phỏng các cảm biến gửi dữ liệu nhiệt độ và độ ẩm định kỳ.

- `monitor_subscriber_bai2.py`:  
  Nhận dữ liệu từ các cảm biến, phân tích JSON và kiểm tra các ngưỡng cảnh báo.

## 3. CÁCH CHẠY CHƯƠNG TRÌNH

**Bước 1: Mở Terminal 1 và chạy Monitoring Subscriber:**

```bash
python monitor_subscriber_bai2.py
```

Chương trình sẽ kết nối tới MQTT Broker và theo dõi dữ liệu  
từ sensor01 và sensor02.

**Bước 2: Mở Terminal 2 và chạy Sensor Publisher:**

```bash
python sensor_publisher_bai2.py
```

Chương trình sẽ mô phỏng cảm biến và gửi dữ liệu mỗi 3 giây.

## 4. ĐỊNH DẠNG DỮ LIỆU

Payload được gửi dưới dạng JSON, gồm các trường:

```json
{
    "device_id": "sensor01",
    "temperature": 28.5,
    "humidity": 65.2
}
```

## 5. KẾT QUẢ ĐẠT ĐƯỢC

- Sensor Publisher kết nối thành công tới MQTT Broker.
- Dữ liệu cảm biến được gửi định kỳ mỗi 3 giây.
- Payload được gửi đúng định dạng JSON.
- Monitoring Subscriber nhận và phân tích được dữ liệu JSON.
- Hiển thị device_id, nhiệt độ và độ ẩm trên màn hình.
- Khi nhiệt độ > 35°C, chương trình hiển thị:
  > "CANH BAO: Nhiet do cao"
- Khi độ ẩm < 40%, chương trình hiển thị:
  > "CANH BAO: Do am thap"
- Chương trình hỗ trợ mô phỏng nhiều thiết bị gồm sensor01 và sensor02.

---

# BÀI 3 - ĐIỀU KHIỂN THIẾT BỊ IOT HAI CHIỀU BẰNG MQTT

## 1. MQTT BROKER SỬ DỤNG

**Broker:** `test.mosquitto.org`  
**Port:** `1883`  
**Protocol:** MQTT

**Các topic sử dụng:**

- `iot/lab/light01/cmd`
- `iot/lab/light01/status`
- `iot/lab/fan01/cmd`
- `iot/lab/fan01/status`
- `iot/lab/pump01/cmd`
- `iot/lab/pump01/status`

## 2. CÁC FILE CHƯƠNG TRÌNH

- `device_bai3.py`:  
  Mô phỏng các thiết bị IoT, nhận lệnh điều khiển ON/OFF  
  và gửi trạng thái của thiết bị về Controller.

- `controller_bai3.py`:  
  Giao diện điều khiển thiết bị, gửi lệnh ON/OFF  
  và nhận trạng thái từ các thiết bị.

## 3. CÁCH CHẠY CHƯƠNG TRÌNH

**Bước 1: Mở Terminal 1 và chạy Device:**

```bash
python device_bai3.py
```

Chương trình sẽ kết nối tới MQTT Broker và theo dõi  
lệnh điều khiển của các thiết bị light01, fan01 và pump01.

**Bước 2: Mở Terminal 2 và chạy Controller:**

```bash
python controller_bai3.py
```

Chương trình sẽ kết nối tới MQTT Broker và hiển thị  
danh sách các thiết bị để người dùng lựa chọn.

## 4. CÁCH ĐIỀU KHIỂN

Controller hỗ trợ các thiết bị:

- `light01`
- `fan01`
- `pump01`

Sau khi chọn thiết bị, người dùng có thể chọn:

- `ON`: Bật thiết bị.
- `OFF`: Tắt thiết bị.
- `HUY`: Hủy thao tác hiện tại.
- `EXIT`: Thoát chương trình Controller.

Ví dụ lệnh điều khiển:

```text
Device: light01
Command: ON
```

Controller gửi:

```text
Topic: iot/lab/light01/cmd
Payload: ON
```

Device nhận lệnh và gửi trạng thái:

```text
Topic: iot/lab/light01/status
```

Payload:

```json
{
  "device_id": "light01",
  "status": "ON"
}
```

## 5. KẾT QUẢ ĐẠT ĐƯỢC

- Device kết nối thành công tới MQTT Broker.
- Controller kết nối thành công tới MQTT Broker.
- Controller gửi được lệnh ON/OFF tới thiết bị.
- Device nhận và xử lý được lệnh điều khiển.
- Device gửi trạng thái hiện tại về Controller.
- Controller nhận và hiển thị được trạng thái thiết bị.
- Chương trình hỗ trợ điều khiển nhiều thiết bị gồm light01, fan01 và pump01.
- Mỗi thiết bị sử dụng topic điều khiển và topic trạng thái riêng.
- Controller có thể tiếp tục điều khiển các thiết bị sau mỗi lần thực hiện lệnh.
- Chương trình hỗ trợ thoát bằng lựa chọn EXIT.

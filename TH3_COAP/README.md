# Báo Cáo Thực Hành: Lập trình Python với giao thức CoAP

## Thông tin sinh viên
- **Họ tên:** Vu Thanh Loc
- **Mã sinh viên:** B23DCCN494

## Môi trường
- **Python:** 3.12
- **Thư viện:** `aiocoap` 0.4.17 (cùng các thư viện chuẩn `asyncio`, `json`, `csv`, `argparse`)
- **Giao thức:** CoAP trên UDP, cổng mặc định `5683`. Không cần broker.

## Cài đặt
```bash
pip install aiocoap
```

## Cấu trúc thư mục
```
TH3_COAP/
|-- bai1/
|   |-- coap_server_bai1.py
|   |-- coap_client_bai1.py
|-- bai2/
|   |-- sensor_server_bai2.py
|   |-- monitor_client_bai2.py
|-- bai3/
|   |-- light_server_bai3.py
|   |-- light_controller_bai3.py
|   |-- light_monitor_bai3.py
|-- README.md
```

## Địa chỉ, cổng và URI tài nguyên
Server mặc định lắng nghe tại `127.0.0.1:5683`. Trên Windows, `aiocoap` không bind được `0.0.0.0`, nên khi chạy Server và Client trên 2 máy khác nhau thì truyền IP LAN của máy Server khi khởi động Server (ví dụ `python light_server_bai3.py 192.168.1.10`), truyền cùng IP đó cho Client và mở tường lửa cho UDP cổng `5683`.

| Bài | URI | Phương thức |
|-----|-----|-------------|
| 1 | `coap://localhost:5683/iot/lab/message` | GET, POST |
| 2 | `coap://localhost:5683/iot/lab/sensor01/data` (thêm `sensor02`, `sensor03`) | GET |
| 3 | `coap://localhost:5683/iot/lab/light01/status` (thêm `fan01`, `pump01`) | GET, PUT, Observe |

## Cách chạy từng chương trình & Kết quả đạt được

### Bài 1: Gửi và nhận thông điệp CoAP cơ bản
1. Terminal 1: `cd bai1` rồi `python coap_server_bai1.py [ip_server]`
2. Terminal 2: `cd bai1` rồi `python coap_client_bai1.py [ip_server]`

**Kết quả:**
- GET trả về `2.05 Content` cùng lời chào của Server.
- POST gửi thông tin sinh viên, Server in nội dung và thời điểm nhận, trả về `2.04 Changed`.
- Mở rộng: Client gửi nhiều POST liên tiếp. Server lưu thông điệp gần nhất và trả kèm trong lần GET sau. Truy cập tài nguyên không tồn tại nhận `4.04 Not Found`. Khi Server không chạy, Client báo lỗi kết nối/timeout thay vì bị treo.

<details>
<summary>Log minh chứng</summary>

Client:
```
Sending GET request...
URI: coap://127.0.0.1:5683/iot/lab/message

Response:
Code: 2.05 Content
Payload: Xin chao tu CoAP Server

Sending POST request...
Payload: Xin chao tu CoAP Client - B23DCCN494 - Vu Thanh Loc

Response:
Code: 2.04 Changed
Payload: Server da nhan thong diep

Sending GET request (sau POST)...
Response:
Code: 2.05 Content
Payload: Xin chao tu CoAP Server | Thong diep gan nhat: Thong diep thu 2 tu Vu Thanh Loc

Sending GET request toi tai nguyen khong ton tai...
URI: coap://127.0.0.1:5683/iot/lab/unknown

Response:
Code: 4.04 Not Found
=> Tai nguyen khong ton tai (4.04 Not Found)
```
Server:
```
CoAP Server started on 127.0.0.1:5683

GET request received: /iot/lab/message

POST request received:
Payload: Xin chao tu CoAP Client - B23DCCN494 - Vu Thanh Loc
Time: 15:28:45
```
Client khi Server không chạy:
```
Sending GET request...
URI: coap://127.0.0.1:5683/iot/lab/message

Loi ket noi toi server: Network error: NetworkError
```
</details>

### Bài 2: Mô phỏng cảm biến nhiệt độ và độ ẩm
1. Terminal 1: `cd bai2` rồi `python sensor_server_bai2.py [ip_server]`
2. Terminal 2: `cd bai2` rồi `python monitor_client_bai2.py [device_id] [ip_server]` (mặc định `sensor01`). Nhấn `Ctrl+C` để dừng.

**Kết quả:**
- Server mô phỏng 3 cảm biến `sensor01`, `sensor02`, `sensor03`. Dữ liệu được sinh ngẫu nhiên lại sau mỗi 3 giây (nhiệt độ 20–40 °C, độ ẩm 30–90 %) và trả về dạng JSON với Content-Format `application/json` (50), có thêm trường `timestamp`.
- Client gửi GET mỗi 3 giây, phân tích JSON và in mã thiết bị, nhiệt độ, độ ẩm, thời điểm nhận. Client cảnh báo khi nhiệt độ > 35 °C hoặc độ ẩm < 40 %.
- Mở rộng: Client chọn được thiết bị cần giám sát, ghi dữ liệu ra `sensor_log_<device_id>.csv`, và khi dừng thì in số lần GET cùng thời gian phản hồi trung bình. Nếu Server ngừng phản hồi, Client báo lỗi và tiếp tục thử lại.

<details>
<summary>Log minh chứng</summary>

```
Monitoring coap://127.0.0.1:5683/iot/lab/sensor02/data (Ctrl+C de dung)

[15:28:53] Received sensor data

Device: sensor02
Temperature: 37.5 C
Humidity: 86.7 %

CANH BAO: Nhiet do cao

------------------------------

[15:28:56] Received sensor data

Device: sensor02
Temperature: 34.8 C
Humidity: 38.8 %

CANH BAO: Do am thap

------------------------------

[15:28:59] Received sensor data

Device: sensor02
Temperature: 27.0 C
Humidity: 64.7 %

Trang thai: Binh thuong

------------------------------

Loi ket noi toi server: Network error: NetworkError     <- đã tắt Server
```
File CSV:
```
received_at,device_id,temperature,humidity,timestamp
15:28:53,sensor02,37.5,86.7,2026-10-21 15:28:51
15:28:56,sensor02,34.8,38.8,2026-10-21 15:28:54
15:28:59,sensor02,27.0,64.7,2026-10-21 15:28:57
```
</details>

### Bài 3: Giám sát và điều khiển đèn thông minh bằng CoAP Observe
1. Terminal 1: `cd bai3` rồi `python light_server_bai3.py [ip_server]`
2. Terminal 2 (có thể mở thêm terminal để chạy nhiều Monitor): `python light_monitor_bai3.py [--device light01] [--server IP]`
3. Terminal 3: `python light_controller_bai3.py [--device light01] [--server IP] [--non]`, sau đó nhập `ON` / `OFF` / `STATUS` / `EXIT`

**Kết quả:**
- Tài nguyên `/iot/lab/light01/status` được cài đặt bằng `ObservableResource`. Trạng thái ban đầu là `OFF`.
- PUT với payload `{"device_id": "light01", "command": "ON"}` cập nhật trạng thái và trả về `2.04 Changed`. Server chỉ gọi `updated_state()` để thông báo cho các observer khi trạng thái **thực sự thay đổi**.
- Monitoring Client đăng ký Observe bằng một GET kèm option `observe=0`, nhận trạng thái ban đầu rồi chờ Server đẩy thông báo. Monitor **không** dùng vòng lặp GET định kỳ.
- Mở rộng:
  - Lệnh không hợp lệ hoặc JSON sai trả về `4.00 Bad Request`.
  - Nhiều Monitor cùng Observe một tài nguyên đều nhận được thông báo.
  - Server có thêm 2 thiết bị `fan01` và `pump01`.
  - Payload có `timestamp`, và các lần đổi trạng thái được ghi vào `device_state_log.txt`.
  - Tùy chọn `--non` gửi request dạng Non-confirmable (NON); mặc định là Confirmable (CON).

<details>
<summary>Log minh chứng</summary>

Terminal 1 – Server (2 Monitor đăng ký):
```
CoAP Smart Light Server started...
Resource: /iot/lab/light01/status
Resource: /iot/lab/fan01/status
Resource: /iot/lab/pump01/status

New Observe registration received (light01, observers: 1)

New Observe registration received (light01, observers: 2)

PUT request received:
Device: light01
Command: ON

Light state changed: OFF -> ON
Notify observers: ON

PUT request received:
Device: light01
Command: ON

Trang thai khong doi (ON), khong gui thong bao

PUT request received:
Device: light01
Command: BLINK

Lenh khong hop le: BLINK

PUT request received:
Device: light01
Command: OFF

Light state changed: ON -> OFF
Notify observers: OFF
```
Terminal 2 – Controller:
```
Nhap lenh (ON/OFF/STATUS/EXIT): ON
Sending PUT request...
Response Code: 2.04 Changed
Da bat den light01

Nhap lenh (ON/OFF/STATUS/EXIT): STATUS
Sending GET request...
Response:
{"device_id": "light01", "status": "ON", "timestamp": "2026-10-21 15:29:20"}

Nhap lenh (ON/OFF/STATUS/EXIT): BLINK
Lenh 'BLINK' khong nam trong ON/OFF/STATUS/EXIT, van gui PUT de kiem tra server...
Response Code: 4.00 Bad Request
Payload: Lenh khong hop le, chi chap nhan ON/OFF

Nhap lenh (ON/OFF/STATUS/EXIT): OFF
Sending PUT request...
Response Code: 2.04 Changed
Da tat den light01
```
Terminal 3 – Monitoring Client (cả 2 Monitor nhận giống nhau):
```
Registering CoAP Observe...
Observe registration successful

[15:29:18] Initial State
Device: light01
Status: OFF

[15:29:20] State Updated
Device: light01
Status: ON

[15:29:24] State Updated
Device: light01
Status: OFF
```
</details>

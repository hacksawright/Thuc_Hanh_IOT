import paho.mqtt.client as mqtt
import json
from datetime import datetime

# MQTT Broker
BROKER = "test.mosquitto.org"
PORT = 1883

# Các topic cần theo dõi
TOPICS = [
    ("iot/lab/sensor01/data", 0),
    ("iot/lab/sensor02/data", 0)
]


# Hàm xử lý khi kết nối tới Broker
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Da ket noi toi MQTT Broker")

        # Subscribe các topic
        for topic, qos in TOPICS:
            client.subscribe(topic, qos)
            print(f"Dang theo doi topic: {topic}")

    else:
        print(f"Ket noi that bai, ma loi: {reason_code}")


# Hàm xử lý khi nhận được message
def on_message(client, userdata, msg):

    try:
        # Chuyển payload từ bytes sang string
        payload = msg.payload.decode("utf-8")

        # Phân tích JSON
        data = json.loads(payload)

        # Lấy dữ liệu
        device_id = data["device_id"]
        temperature = data["temperature"]
        humidity = data["humidity"]

        # Thời gian nhận dữ liệu
        receive_time = datetime.now().strftime("%H:%M:%S")

        print("\n" + "=" * 40)
        print(f"Time: {receive_time}")
        print(f"Device: {device_id}")
        print(f"Temperature: {temperature} C")
        print(f"Humidity: {humidity} %")

        # Kiểm tra ngưỡng nhiệt độ
        if temperature > 35:
            print("CANH BAO: Nhiet do cao")

        # Kiểm tra ngưỡng độ ẩm
        if humidity < 40:
            print("CANH BAO: Do am thap")

        print("=" * 40)

    except json.JSONDecodeError:
        print("Loi: Payload khong phai JSON hop le.")

    except KeyError as e:
        print(f"Loi: Thieu truong {e}")


# Tạo MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Đăng ký callback
client.on_connect = on_connect
client.on_message = on_message

print("Dang ket noi toi MQTT Broker ...")

try:
    # Kết nối tới Broker
    client.connect(BROKER, PORT, 60)

    # Chạy liên tục cho đến khi Ctrl+C
    client.loop_forever()

except KeyboardInterrupt:
    print("\nDung monitoring subscriber...")

except ConnectionRefusedError:
    print("Khong the ket noi toi MQTT Broker.")

except Exception as e:
    print(f"Co loi xay ra: {e}")

finally:
    client.disconnect()
    print("Da ngat ket noi.")
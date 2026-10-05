import paho.mqtt.client as mqtt
import json

# MQTT Broker
BROKER = "test.mosquitto.org"
PORT = 1883

# Danh sách thiết bị
DEVICES = ["light01", "fan01", "pump01"]

# Lưu trạng thái của các thiết bị
device_status = {
    "light01": "OFF",
    "fan01": "OFF",
    "pump01": "OFF"
}


# Hàm xử lý khi kết nối tới Broker
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Da ket noi toi MQTT Broker")

        # Subscribe topic điều khiển của tất cả thiết bị
        for device_id in DEVICES:
            topic = f"iot/lab/{device_id}/cmd"
            client.subscribe(topic)
            print(f"Dang lang nghe: {topic}")

        print("\nTrang thai ban dau:")
        for device_id in DEVICES:
            print(f"- {device_id}: {device_status[device_id]}")

    else:
        print(f"Ket noi that bai, ma loi: {reason_code}")


# Hàm xử lý khi nhận được lệnh
def on_message(client, userdata, msg):
    global device_status

    # Lấy device_id từ topic
    # Ví dụ: iot/lab/light01/cmd
    parts = msg.topic.split("/")
    device_id = parts[2]

    # Đọc lệnh
    command = msg.payload.decode("utf-8").strip().upper()

    print(f"\nNhan duoc lenh:")
    print(f"Device: {device_id}")
    print(f"Command: {command}")

    # Kiểm tra thiết bị
    if device_id not in DEVICES:
        print("Thiet bi khong ton tai!")
        return

    # Xử lý lệnh
    if command == "ON":
        device_status[device_id] = "ON"

    elif command == "OFF":
        device_status[device_id] = "OFF"

    else:
        print(f"Lenh khong hop le: {command}")
        return

    # Tạo payload trạng thái
    status_data = {
        "device_id": device_id,
        "status": device_status[device_id]
    }

    status_payload = json.dumps(status_data)

    # Topic trạng thái
    status_topic = f"iot/lab/{device_id}/status"

    # Publish trạng thái
    result = client.publish(status_topic, status_payload)

    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"Da cap nhat {device_id}: {device_status[device_id]}")
        print(f"Da gui trang thai: {status_payload}")
    else:
        print("Gui trang thai that bai!")


# Tạo MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Đăng ký callback
client.on_connect = on_connect
client.on_message = on_message

print("Smart Device System")
print("===================")
print("Dang ket noi toi MQTT Broker ...")

try:
    client.connect(BROKER, PORT, 60)

    # Chạy liên tục
    client.loop_forever()

except KeyboardInterrupt:
    print("\nDung Smart Device System...")

except ConnectionRefusedError:
    print("Khong the ket noi toi MQTT Broker.")

except Exception as e:
    print(f"Co loi xay ra: {e}")

finally:
    client.disconnect()
    print("Da ngat ket noi.")
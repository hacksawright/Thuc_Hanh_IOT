import paho.mqtt.client as mqtt
import time

# MQTT Broker
BROKER = "test.mosquitto.org"
PORT = 1883

# MQTT Topic
TOPIC = "iot/lab/message"

# Thông tin các thành viên trong nhóm
MEMBERS = [
    ("B23DCCN858", "Nguyen Duc Trung"),
    ("B23DCCN494", "Vu Thanh Loc"),
    ("B23DCCN944", "Nguyen Manh Vu")
]

# Tạo MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

print("Dang ket noi toi MQTT Broker ...")

try:
    # Kết nối tới Broker
    client.connect(BROKER, PORT, 60)

    print("Ket noi thanh cong")

    # Chạy MQTT network loop ở background
    client.loop_start()

    # Gửi nhiều message liên tiếp
    for i in range(1, 6):

        # Chọn thành viên theo thứ tự
        student_id, name = MEMBERS[(i - 1) % len(MEMBERS)]

        message = (
            f"Xin chao tu client Python MQTT - "
            f"{student_id} - {name}"
        )

        # Publish message
        result = client.publish(TOPIC, message)

        # Đảm bảo message đã được gửi
        result.wait_for_publish()

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"\nDa gui message {i}:")
            print(f"Topic: {TOPIC}")
            print(f"Payload: {message}")
        else:
            print(f"Gui message {i} that bai!")

        # Chờ trước khi gửi message tiếp theo
        time.sleep(2)

except KeyboardInterrupt:
    print("\nDung publisher...")

except ConnectionRefusedError:
    print("Khong the ket noi toi MQTT Broker.")

finally:
    client.loop_stop()
    client.disconnect()
    print("\nDa ngat ket noi.")
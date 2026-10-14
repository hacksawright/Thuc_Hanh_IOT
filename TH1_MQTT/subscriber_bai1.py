import paho.mqtt.client as mqtt
from datetime import datetime

# MQTT Broker
BROKER = "test.mosquitto.org"
PORT = 1883

# MQTT Topic
TOPIC = "iot/lab/message"


# Hàm xử lý khi kết nối tới Broker
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Da ket noi toi MQTT Broker")
        client.subscribe(TOPIC)
        print(f"Dang lang nghe topic: {TOPIC}")
    else:
        print(f"Ket noi that bai, ma loi: {reason_code}")


# Hàm xử lý khi nhận được message
def on_message(client, userdata, msg):
    receive_time = datetime.now().strftime("%H:%M:%S")
    payload = msg.payload.decode("utf-8")

    print("\nNhan duoc message:")
    print(f"Topic: {msg.topic}")
    print(f"Payload: {payload}")
    print(f"Time: {receive_time}")


# Tạo MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Đăng ký callback
client.on_connect = on_connect
client.on_message = on_message

print("Dang ket noi toi MQTT Broker ...")

try:
    client.connect(BROKER, PORT, 60)

    # Chạy liên tục cho đến khi nhấn Ctrl+C
    client.loop_forever()

except KeyboardInterrupt:
    print("\nDung subscriber...")

except ConnectionRefusedError:
    print("Khong the ket noi toi MQTT Broker.")

finally:
    client.disconnect()
    print("Da ngat ket noi.")
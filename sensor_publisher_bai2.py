import paho.mqtt.client as mqtt
import json
import random
import time

# MQTT Broker
BROKER = "test.mosquitto.org"
PORT = 1883

# Danh sách thiết bị
DEVICES = [
    "sensor01",
    "sensor02"
]

# Tạo MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

print("Dang ket noi toi MQTT Broker ...")

try:
    # Kết nối tới Broker
    client.connect(BROKER, PORT, 60)

    print("Ket noi thanh cong")

    # Chạy MQTT network loop
    client.loop_start()

    device_index = 0

    while True:
        # Chọn thiết bị
        device_id = DEVICES[device_index]

        # Topic tương ứng với thiết bị
        topic = f"iot/lab/{device_id}/data"

        # Sinh dữ liệu cảm biến ngẫu nhiên
        temperature = round(random.uniform(25, 40), 1)
        humidity = round(random.uniform(30, 80), 1)

        # Tạo payload JSON
        data = {
            "device_id": device_id,
            "temperature": temperature,
            "humidity": humidity
        }

        # Chuyển dữ liệu sang JSON
        payload = json.dumps(data)

        # Kiểm tra kết nối
        if not client.is_connected():
            print("Client da mat ket noi. Dang ket noi lai...")
            client.reconnect()

        # Publish dữ liệu
        result = client.publish(topic, payload)

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print("\nDa gui du lieu:")
            print(f"Topic: {topic}")
            print(f"Device: {device_id}")
            print(f"Temperature: {temperature} C")
            print(f"Humidity: {humidity} %")
            print(f"Payload: {payload}")
        else:
            print(f"Gui du lieu that bai: {result.rc}")

        # Chuyển sang thiết bị tiếp theo
        device_index = (device_index + 1) % len(DEVICES)

        # Gửi dữ liệu mỗi 3 giây
        time.sleep(3)

except KeyboardInterrupt:
    print("\nDung sensor publisher...")

except Exception as e:
    print(f"\nCo loi xay ra: {e}")

finally:
    client.loop_stop()
    client.disconnect()
    print("Da ngat ket noi.")
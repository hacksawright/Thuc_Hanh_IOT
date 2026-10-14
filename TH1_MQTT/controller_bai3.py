import paho.mqtt.client as mqtt
import json
import time

# MQTT Broker
BROKER = "test.mosquitto.org"
PORT = 1883

# Danh sách thiết bị
DEVICES = [
    "light01",
    "fan01",
    "pump01"
]


# Hàm xử lý khi kết nối tới Broker
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Da ket noi toi MQTT Broker")

        # Subscribe trạng thái của tất cả thiết bị
        for device_id in DEVICES:
            topic = f"iot/lab/{device_id}/status"
            client.subscribe(topic)

        print("Da dang ky theo doi trang thai cac thiet bi.")

    else:
        print(f"Ket noi that bai, ma loi: {reason_code}")


# Hàm xử lý khi nhận trạng thái
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        print("\n--- Trang thai nhan duoc ---")
        print(f"Device: {data['device_id']}")
        print(f"Status: {data['status']}")
        print(f"Payload: {payload}")
        print("----------------------------")

    except json.JSONDecodeError:
        print("Payload khong phai JSON hop le.")

    except KeyError as e:
        print(f"Payload thieu truong: {e}")


# Tạo MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Đăng ký callback
client.on_connect = on_connect
client.on_message = on_message

print("Controller App")
print("==============")

try:
    # Kết nối tới Broker
    client.connect(BROKER, PORT, 60)

    # Chạy MQTT network loop ở background
    client.loop_start()

    # Chờ kết nối hoàn tất
    time.sleep(2)

    # Vòng lặp điều khiển
    while True:

        # =========================
        # BƯỚC 1: CHỌN THIẾT BỊ
        # =========================
        print("\nDanh sach thiet bi:")
        print("1. light01")
        print("2. fan01")
        print("3. pump01")
        print("4. EXIT")

        device_input = input("Chon thiet bi: ").strip().lower()

        # Thoát chương trình
        if device_input == "4" or device_input == "exit":
            print("Dang thoat Controller App...")
            break

        # Kiểm tra thiết bị
        if device_input not in DEVICES:
            print("Loi: Thiet bi khong hop le!")
            continue

        # =========================
        # BƯỚC 2: CHỌN TRẠNG THÁI
        # =========================
        print(f"\nThiet bi da chon: {device_input}")
        print("1. ON")
        print("2. OFF")
        print("3. HUY")

        command_input = input("Chon trang thai: ").strip().upper()

        # Hủy thao tác, quay lại chọn thiết bị
        if command_input == "3" or command_input == "HUY":
            continue

        # Kiểm tra lệnh
        if command_input not in ["ON", "OFF"]:
            print("Loi: Trang thai khong hop le!")
            continue

        # =========================
        # BƯỚC 3: GỬI LỆNH
        # =========================

        # Kiểm tra kết nối
        if not client.is_connected():
            print("Client da mat ket noi. Dang ket noi lai...")
            client.reconnect()
            time.sleep(1)

        # Topic điều khiển
        cmd_topic = f"iot/lab/{device_input}/cmd"

        # Publish lệnh
        result = client.publish(cmd_topic, command_input)

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"\nDa gui lenh {command_input} toi {device_input}")
            print(f"Topic: {cmd_topic}")
        else:
            print("Gui lenh that bai!")

        # Chờ một chút để nhận phản hồi
        time.sleep(1)

        # while True sẽ tự động quay lại
        # bước chọn thiết bị


except KeyboardInterrupt:
    print("\nDung Controller App...")

except ConnectionRefusedError:
    print("Khong the ket noi toi MQTT Broker.")

except Exception as e:
    print(f"Co loi xay ra: {e}")

finally:
    client.loop_stop()
    client.disconnect()
    print("Da ngat ket noi.")
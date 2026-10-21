import asyncio
import json
import sys
from datetime import datetime

import aiocoap
import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat

#Windows không bind được 0.0.0.0 -> mặc định 127.0.0.1, chạy 2 máy thì truyền IP LAN của máy server
HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 5683
DEVICES = ["light01", "fan01", "pump01"]
LOG_FILE = "device_state_log.txt"
VALID_COMMANDS = ("ON", "OFF")


def write_log(line):
    #Ghi nhật ký thay đổi trạng thái thiết bị ra file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {line}\n")


def error(code, text):
    return aiocoap.Message(code=code, payload=text.encode("utf-8"))


class DeviceStatusResource(resource.ObservableResource):
    """Tài nguyên /iot/lab/<device_id>/status hỗ trợ GET, PUT và Observe."""

    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        self.status = "OFF"  # trạng thái ban đầu
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.observer_count = 0

    def update_observation_count(self, count):
        #aiocoap gọi hàm này mỗi khi có client đăng ký/hủy Observe
        if count > self.observer_count:
            print(f"New Observe registration received ({self.device_id}, observers: {count})\n")
        elif count < self.observer_count:
            print(f"Observe cancelled ({self.device_id}, observers: {count})\n")
        self.observer_count = count

    def state_payload(self):
        return json.dumps({
            "device_id": self.device_id,
            "status": self.status,
            "timestamp": self.updated_at,
        }).encode("utf-8")

    async def render_get(self, request):
        #Dùng chung cho GET thường và các thông báo Observe
        return aiocoap.Message(code=aiocoap.CONTENT, payload=self.state_payload(),
                               content_format=ContentFormat.JSON)

    async def render_put(self, request):
        try:
            data = json.loads(request.payload.decode("utf-8"))
            device_id = data["device_id"]
            command = str(data["command"]).upper()
        except (ValueError, KeyError, TypeError):
            print("PUT request received: payload khong hop le\n")
            return error(aiocoap.BAD_REQUEST, "Payload JSON khong hop le")

        print("PUT request received:")
        print(f"Device: {device_id}")
        print(f"Command: {command}\n")

        if device_id != self.device_id:
            return error(aiocoap.BAD_REQUEST, f"device_id phai la {self.device_id}")
        if command not in VALID_COMMANDS:
            print(f"Lenh khong hop le: {command}\n")
            return error(aiocoap.BAD_REQUEST, "Lenh khong hop le, chi chap nhan ON/OFF")

        old = self.status
        if command != old:
            self.status = command
            self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            label = "Light" if self.device_id.startswith("light") else self.device_id
            print(f"{label} state changed: {old} -> {command}")
            write_log(f"{self.device_id}: {old} -> {command}")
            #Chỉ thông báo cho các observer khi trạng thái thực sự thay đổi
            self.updated_state()
            print(f"Notify observers: {command}\n")
        else:
            print(f"Trang thai khong doi ({old}), khong gui thong bao\n")

        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.state_payload(),
                               content_format=ContentFormat.JSON)


async def main():
    site = resource.Site()
    for device_id in DEVICES:
        site.add_resource(["iot", "lab", device_id, "status"], DeviceStatusResource(device_id))

    await aiocoap.Context.create_server_context(site, bind=(HOST, PORT))
    print("CoAP Smart Light Server started...")
    for device_id in DEVICES:
        print(f"Resource: /iot/lab/{device_id}/status")
    print()

    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped")

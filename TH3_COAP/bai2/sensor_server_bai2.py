import asyncio
import json
import random
import sys
from datetime import datetime

import aiocoap
import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat

#Windows không bind được 0.0.0.0 -> mặc định 127.0.0.1, chạy 2 máy thì truyền IP LAN của máy server
HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 5683
UPDATE_INTERVAL = 3  # giây
DEVICES = ["sensor01", "sensor02", "sensor03"]


class SensorDataResource(resource.Resource):
    """Tài nguyên /iot/lab/<device_id>/data trả về dữ liệu cảm biến mới nhất (JSON)."""

    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        self.data = {}
        self.update()

    def update(self):
        #Sinh giá trị ngẫu nhiên trong khoảng hợp lý
        self.data = {
            "device_id": self.device_id,
            "temperature": round(random.uniform(20.0, 40.0), 1),
            "humidity": round(random.uniform(30.0, 90.0), 1),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    async def render_get(self, request):
        print(f"GET /iot/lab/{self.device_id}/data -> {self.data}")
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=json.dumps(self.data).encode("utf-8"),
            content_format=ContentFormat.JSON,
        )


async def update_loop(sensors):
    #Cập nhật dữ liệu cho tất cả cảm biến sau mỗi 3 giây
    while True:
        await asyncio.sleep(UPDATE_INTERVAL)
        for sensor in sensors:
            sensor.update()


async def main():
    site = resource.Site()
    sensors = []
    for device_id in DEVICES:
        sensor = SensorDataResource(device_id)
        sensors.append(sensor)
        site.add_resource(["iot", "lab", device_id, "data"], sensor)

    await aiocoap.Context.create_server_context(site, bind=(HOST, PORT))
    print(f"Sensor CoAP Server started on {HOST}:{PORT}")
    for device_id in DEVICES:
        print(f"Resource: /iot/lab/{device_id}/data")
    print()

    await update_loop(sensors)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped")

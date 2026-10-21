import asyncio
import csv
import json
import os
import sys
import time
from datetime import datetime

import aiocoap

#Cách dùng: python monitor_client_bai2.py [device_id] [server_ip]
DEVICE_ID = sys.argv[1] if len(sys.argv) > 1 else "sensor01"
SERVER = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
URI = f"coap://{SERVER}:5683/iot/lab/{DEVICE_ID}/data"
POLL_INTERVAL = 3  # giây
TIMEOUT = 10  # giây
CSV_FILE = f"sensor_log_{DEVICE_ID}.csv"


def save_csv(row):
    #Ghi dữ liệu nhận được ra file CSV để phân tích
    new_file = not os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["received_at", "device_id", "temperature", "humidity", "timestamp"])
        writer.writerow(row)


def show(data, received_at):
    print(f"[{received_at}] Received sensor data\n")
    print(f"Device: {data['device_id']}")
    print(f"Temperature: {data['temperature']} C")
    print(f"Humidity: {data['humidity']} %\n")

    warnings = []
    if data["temperature"] > 35:
        warnings.append("CANH BAO: Nhiet do cao")
    if data["humidity"] < 40:
        warnings.append("CANH BAO: Do am thap")

    if warnings:
        print("\n".join(warnings))
    else:
        print("Trang thai: Binh thuong")


async def main():
    context = await aiocoap.Context.create_client_context()
    print(f"Monitoring {URI} (Ctrl+C de dung)\n")

    request_count = 0
    success_count = 0
    total_rtt = 0.0

    try:
        while True:
            request_count += 1
            start = time.perf_counter()
            try:
                request = aiocoap.Message(code=aiocoap.GET, uri=URI)
                response = await asyncio.wait_for(context.request(request).response, TIMEOUT)
            except asyncio.TimeoutError:
                print(f"Loi: Server khong phan hoi sau {TIMEOUT} giay")
            except aiocoap.error.Error as e:
                print(f"Loi ket noi toi server: {e}")
            else:
                rtt = (time.perf_counter() - start) * 1000
                received_at = datetime.now().strftime("%H:%M:%S")

                if response.code.is_successful():
                    try:
                        data = json.loads(response.payload.decode("utf-8"))
                        show(data, received_at)
                        save_csv([received_at, data["device_id"], data["temperature"],
                                  data["humidity"], data.get("timestamp", "")])
                        success_count += 1
                        total_rtt += rtt
                    except (ValueError, KeyError) as e:
                        print(f"Loi: Du lieu JSON khong hop le ({e})")
                else:
                    print(f"Loi: Server tra ve {response.code} - "
                          f"{response.payload.decode('utf-8', errors='replace')}")

            print("\n------------------------------\n")
            await asyncio.sleep(POLL_INTERVAL)
    finally:
        #Thống kê số lần GET và thời gian phản hồi trung bình
        print("\nThong ke:")
        print(f"So lan GET: {request_count}, thanh cong: {success_count}")
        if success_count:
            print(f"Thoi gian phan hoi trung binh: {total_rtt / success_count:.2f} ms")
        print(f"Du lieu da ghi vao: {CSV_FILE}")
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Da dung giam sat")

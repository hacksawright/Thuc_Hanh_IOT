import argparse
import asyncio
import json

import aiocoap

TIMEOUT = 10  # giây

parser = argparse.ArgumentParser(description="Light Controller Client (CoAP GET/PUT)")
parser.add_argument("--device", default="light01", help="light01 / fan01 / pump01")
parser.add_argument("--server", default="127.0.0.1", help="IP cua CoAP Server")
parser.add_argument("--non", action="store_true",
                    help="Gui request dang Non-confirmable (NON) thay vi Confirmable (CON)")
args = parser.parse_args()

URI = f"coap://{args.server}:5683/iot/lab/{args.device}/status"
#NON: không cần ACK, không gửi lại; CON: chờ ACK và tự gửi lại khi mất gói
TUNING = aiocoap.Unreliable if args.non else aiocoap.Reliable


async def send(context, request):
    try:
        return await asyncio.wait_for(context.request(request).response, TIMEOUT)
    except asyncio.TimeoutError:
        print(f"Loi: Server khong phan hoi sau {TIMEOUT} giay\n")
    except aiocoap.error.Error as e:
        print(f"Loi ket noi toi server: {e}\n")
    return None


async def main():
    context = await aiocoap.Context.create_client_context()
    loop = asyncio.get_running_loop()
    print(f"Controller ket noi toi {URI} (kieu message: {'NON' if args.non else 'CON'})\n")

    while True:
        #Đọc bàn phím trong thread riêng để không chặn event loop
        try:
            line = await loop.run_in_executor(None, input, "Nhap lenh (ON/OFF/STATUS/EXIT): ")
        except EOFError:
            break
        command = line.strip().upper()
        print()

        if command == "EXIT":
            break

        if command in ("ON", "OFF"):
            print("Sending PUT request...")
            payload = json.dumps({"device_id": args.device, "command": command}).encode("utf-8")
            request = aiocoap.Message(code=aiocoap.PUT, transport_tuning=TUNING, uri=URI, payload=payload)
            response = await send(context, request)
            if response is None:
                continue
            print(f"Response Code: {response.code}")
            if response.code == aiocoap.CHANGED:
                print(f"Da {'bat' if command == 'ON' else 'tat'} den {args.device}\n")
            else:
                print(f"Loi: {response.payload.decode('utf-8', errors='replace')}\n")

        elif command == "STATUS":
            print("Sending GET request...")
            request = aiocoap.Message(code=aiocoap.GET, transport_tuning=TUNING, uri=URI)
            response = await send(context, request)
            if response is None:
                continue
            print("Response:")
            print(response.payload.decode("utf-8", errors="replace") + "\n")

        elif command:
            #Gửi lệnh tùy ý lên server để kiểm tra xử lý lệnh không hợp lệ
            print(f"Lenh '{command}' khong nam trong ON/OFF/STATUS/EXIT, van gui PUT de kiem tra server...")
            payload = json.dumps({"device_id": args.device, "command": command}).encode("utf-8")
            response = await send(context, aiocoap.Message(code=aiocoap.PUT, transport_tuning=TUNING,
                                                           uri=URI, payload=payload))
            if response is not None:
                print(f"Response Code: {response.code}")
                print(f"Payload: {response.payload.decode('utf-8', errors='replace')}\n")

    print("Ket thuc chuong trinh")
    await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nKet thuc chuong trinh")

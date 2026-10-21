import argparse
import asyncio
import json
from datetime import datetime

import aiocoap

TIMEOUT = 10  # giây

parser = argparse.ArgumentParser(description="Light Monitoring Client (CoAP Observe)")
parser.add_argument("--device", default="light01", help="light01 / fan01 / pump01")
parser.add_argument("--server", default="127.0.0.1", help="IP cua CoAP Server")
args = parser.parse_args()

URI = f"coap://{args.server}:5683/iot/lab/{args.device}/status"


def show(title, response):
    try:
        data = json.loads(response.payload.decode("utf-8"))
    except ValueError:
        print(f"Loi: payload khong phai JSON: {response.payload!r}\n")
        return
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {title}")
    print(f"Device: {data.get('device_id')}")
    print(f"Status: {data.get('status')}\n")


async def main():
    context = await aiocoap.Context.create_client_context()

    #Gửi GET kèm option Observe=0 để đăng ký theo dõi (không polling)
    print("Registering CoAP Observe...")
    request = context.request(aiocoap.Message(code=aiocoap.GET, uri=URI, observe=0))

    try:
        response = await asyncio.wait_for(request.response, TIMEOUT)
    except asyncio.TimeoutError:
        print(f"Loi: Server khong phan hoi sau {TIMEOUT} giay")
        await context.shutdown()
        return
    except aiocoap.error.Error as e:
        print(f"Loi ket noi toi server: {e}")
        await context.shutdown()
        return

    if not response.code.is_successful():
        print(f"Loi: Server tra ve {response.code}")
        await context.shutdown()
        return
    if response.opt.observe is None:
        print("Server khong ho tro Observe cho tai nguyen nay")
        await context.shutdown()
        return

    print("Observe registration successful\n")
    show("Initial State", response)

    #Server tự đẩy thông báo mỗi khi trạng thái thay đổi
    try:
        async for notification in request.observation:
            show("State Updated", notification)
        print("Server da ket thuc Observe")
    except aiocoap.error.Error as e:
        print(f"Mat ket noi Observe: {e}")
    finally:
        if not request.observation.cancelled:
            request.observation.cancel()
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDa dung theo doi")

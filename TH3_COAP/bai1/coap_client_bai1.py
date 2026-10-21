import asyncio
import sys

import aiocoap

#Có thể truyền IP server qua tham số: python coap_client_bai1.py 192.168.1.10
SERVER = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
BASE_URI = f"coap://{SERVER}:5683"
TIMEOUT = 10  # giây

student_id = "B23DCCN494"
student_name = "Vu Thanh Loc"


async def send(context, code, path, payload=b""):
    """Gửi một request, in kết quả; trả về None nếu lỗi kết nối/timeout."""
    uri = BASE_URI + path
    request = aiocoap.Message(code=code, uri=uri, payload=payload)
    try:
        response = await asyncio.wait_for(context.request(request).response, TIMEOUT)
    except asyncio.TimeoutError:
        print(f"Loi: Server khong phan hoi sau {TIMEOUT} giay (timeout)\n")
        return None
    except aiocoap.error.Error as e:
        print(f"Loi ket noi toi server: {e}\n")
        return None

    print("Response:")
    print(f"Code: {response.code}")
    print(f"Payload: {response.payload.decode('utf-8', errors='replace')}\n")
    return response


async def main():
    context = await aiocoap.Context.create_client_context()
    print("CoAP Client\n")

    #GET lời chào từ server
    print("Sending GET request...")
    print(f"URI: {BASE_URI}/iot/lab/message\n")
    if await send(context, aiocoap.GET, "/iot/lab/message") is None:
        await context.shutdown()
        return

    #Gửi nhiều thông điệp POST liên tiếp
    messages = [
        f"Xin chao tu CoAP Client - {student_id} - {student_name}",
        f"Thong diep thu 2 tu {student_name}",
    ]
    for msg in messages:
        print("Sending POST request...")
        print(f"Payload: {msg}\n")
        await send(context, aiocoap.POST, "/iot/lab/message", msg.encode("utf-8"))

    #GET lại để nhận thông điệp POST gần nhất mà server lưu
    print("Sending GET request (sau POST)...")
    await send(context, aiocoap.GET, "/iot/lab/message")

    #Thử truy cập tài nguyên không tồn tại
    print("Sending GET request toi tai nguyen khong ton tai...")
    print(f"URI: {BASE_URI}/iot/lab/unknown\n")
    response = await send(context, aiocoap.GET, "/iot/lab/unknown")
    if response is not None and response.code == aiocoap.NOT_FOUND:
        print("=> Tai nguyen khong ton tai (4.04 Not Found)\n")

    await context.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

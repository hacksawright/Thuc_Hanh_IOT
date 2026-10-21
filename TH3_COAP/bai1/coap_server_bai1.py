import asyncio
import sys
from datetime import datetime

import aiocoap
import aiocoap.resource as resource

#Windows không bind được 0.0.0.0 -> mặc định 127.0.0.1, chạy 2 máy thì truyền IP LAN của máy server
HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 5683


class MessageResource(resource.Resource):
    """Tài nguyên /iot/lab/message: GET trả về lời chào, POST nhận thông điệp."""

    def __init__(self):
        super().__init__()
        #Lưu lại thông điệp POST gần nhất
        self.last_message = None

    async def render_get(self, request):
        print("GET request received: /iot/lab/message\n")

        text = "Xin chao tu CoAP Server"
        if self.last_message:
            text += f" | Thong diep gan nhat: {self.last_message}"
        return aiocoap.Message(code=aiocoap.CONTENT, payload=text.encode("utf-8"))

    async def render_post(self, request):
        text = request.payload.decode("utf-8", errors="replace").strip()
        if not text:
            return aiocoap.Message(code=aiocoap.BAD_REQUEST,
                                   payload=b"Payload rong")

        self.last_message = text
        print("POST request received:")
        print(f"Payload: {text}")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}\n")

        return aiocoap.Message(code=aiocoap.CHANGED,
                               payload="Server da nhan thong diep".encode("utf-8"))


async def main():
    #Khai báo cây tài nguyên của server
    site = resource.Site()
    site.add_resource(["iot", "lab", "message"], MessageResource())

    await aiocoap.Context.create_server_context(site, bind=(HOST, PORT))
    print(f"CoAP Server started on {HOST}:{PORT}\n")

    #Giữ server chạy mãi
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped")

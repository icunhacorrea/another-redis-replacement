from asyncio import Semaphore, StreamReader, StreamWriter

from arr.core.memory import Memory
from arr.core.resp import Resp

class Handler:

    def __init__(self, semaphore: Semaphore, mem: Memory) -> None:
        self.semaphore = semaphore
        self.mem = mem
        self.resp = Resp()

    async def handle_client(self, reader: StreamReader, writer: StreamWriter):

        addr = writer.get_extra_info("peername")
        print(f"Connection from: {addr}")

        async with self.semaphore:
            try:
                while True:
                    data = await reader.read(100)
                    
                    if not data:
                        break

                    message = await self.process_data(data, addr=addr)
                    await self.write_response(writer, response=message)
            except ConnectionResetError as err:
                print(f"Connection lost with {addr}: {err}")
            finally:
                writer.close()
                await writer.wait_closed()
                print(f"Connection from {addr} closed.")

    async def read_data(self, reader: StreamReader) -> bytes:
        return await reader.read(100)

    async def write_response(self, writer: StreamWriter, response: str) -> None:
        writer.write(response.encode())
        await writer.drain()
    
    async def process_data(self, data: bytes, addr: str) -> str:
        print("Data: ", data)
        self.resp.decode_data(data)
        return "+world\r\n"


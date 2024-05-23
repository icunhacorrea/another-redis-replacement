from asyncio import Semaphore, StreamReader, StreamWriter

from arr.core.memory import Memory
from arr.core.resp import Resp

class Handler:

    def __init__(self, semaphore: Semaphore, mem: Memory) -> None:
        self.semaphore = semaphore
        self.mem = mem
        self.resp = Resp(self.mem)

    async def handle_client(self, reader: StreamReader, writer: StreamWriter):

        addr = writer.get_extra_info("peername")
        print(f"Connection from: {addr}")

        async with self.semaphore:
            try:
                while True:
                    data = await reader.read(100)
                    self.show_data(data=data)
                    
                    if not data:
                        break

                    response = await self.process_data(data, addr=addr)
                    await self.write_response(writer, response=response)
                    self.show_mem()
            except ConnectionResetError as err:
                print(f"Connection lost with {addr}: {err}")
                raise err
            finally:
                writer.close()
                await writer.wait_closed()
                print(f"Connection from {addr} closed.")

    async def read_data(self, reader: StreamReader) -> bytes:
        return await reader.read(100)

    async def write_response(self, writer: StreamWriter, response: bytes) -> None:
        writer.write(response)
        await writer.drain()
    
    async def process_data(self, data: bytes, addr: str) -> bytes:
        response = await self.resp.deserialize_request(data)
        print(f"Response to client addr={addr}: {response}")
        return response

    def show_mem(self):
        print(f"{self.mem}")

    def show_data(self, data: bytes) -> None:
        print(f"Data: {data}")


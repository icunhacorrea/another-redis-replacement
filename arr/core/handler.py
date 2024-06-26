from asyncio import Semaphore, StreamReader, StreamWriter
from arr.core.database.dicth import DictH
from arr.core.resp import Resp

class Handler:

    def __init__(self, semaphore: Semaphore, dicth: DictH) -> None:
        self.semaphore = semaphore
        self.dicth = dicth
        self.resp = Resp(self.dicth)

    async def handle_client(self, reader: StreamReader, writer: StreamWriter):
        addr = writer.get_extra_info("peername")
        print(f"Connection from: {addr}")

        async with self.semaphore:
            try:
                while True:
                    data = await reader.read(4096)
                    #self.show_data(data=data)
                    
                    if not data:
                        break

                    response = await self.process_data(data, addr=addr)
                    await self.write_response(writer, response=response)
                    #self.show_mem()
                    self.dicth.print_list()
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
        return response

    def show_mem(self):
        print(f"{self.mem}")

    def show_data(self, data: bytes) -> None:
        print(f"Data: {data}")

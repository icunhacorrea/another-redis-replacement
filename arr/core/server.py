import socket
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from asyncio import Semaphore, start_server as start_server_asyncio
from arr.core.handler import Handler
from arr.core.memory import Memory

class Server:

    def __init__(self,
                 port: int  = 7070,
                 host: str = "localhost",
                 max_clients: int = 1) -> None:
        self.port = port
        self.host = host
        self.mem = Memory()
        self.handler = Handler()
        self.semaphore = Semaphore(max_clients)

    async def start_server(self) -> None:

        server = await start_server_asyncio(Handler.handle_client, self.host, self.port)

        async with server as s:
            print(f"Initing server: {server}")
            await s.serve_forever()

    def print_hi(self) -> None:
        print("hi")


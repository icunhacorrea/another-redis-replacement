import socket
from asyncio import Semaphore, start_server as start_server_asyncio
from arr.core.database.dicth import DictH
from arr.core.handler import Handler
from arr.core.memory import Memory

class Server:

    def __init__(self,
                 port: int  = 7070,
                 host: str = "localhost",
                 max_clients: int = 50) -> None:
        self.port = port
        self.host = host
        self.mem = Memory()
        self.dicth = DictH(max_size=100)
        self.semaphore = Semaphore(max_clients)
        self.handler = Handler(self.semaphore, self.mem, self.dicth)

    async def start_server(self) -> None:

        server = await start_server_asyncio(self.handler.handle_client, self.host, self.port)

        for s in server.sockets:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*4096*1024)
            # s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024*4096*1024)
            # s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            # s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 30)  # Intervalo em segundos entre os pacotes de keepalive
            # s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)


        recv_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        print("Tamanho do buffer de recebimento:", recv_buffer_size)

        async with server as s:
            print(f"Initing server: {server}")
            await s.serve_forever()

    def print_hi(self) -> None:
        print("hi")

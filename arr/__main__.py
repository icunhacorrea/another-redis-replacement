import asyncio

from uvloop import EventLoopPolicy
from arr.core.server import Server

asyncio.set_event_loop_policy(EventLoopPolicy())

async def main():
    server = Server()
    await server.start_server()

if __name__ == "__main__":
    asyncio.run(main())


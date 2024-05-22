import asyncio
from arr.core.server import (
    Server
)

async def main():
    server = Server()
    await server.start_server()

if __name__ == "__main__":
    asyncio.run(main())

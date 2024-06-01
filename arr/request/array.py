from typing import Any
from arr.core.database.dicth import DictH
from arr.core.database.entry import Entry
from arr.request.base import Request

class ArrayRequest(Request):
    def __init__(self, dicth: DictH, data: bytes) -> None:
        super(ArrayRequest, self).__init__(data)
        self.array = []
        self.dicth = dicth
        self.process_array()

    def process_array(self) -> None:
        in_arr = self.data.decode().strip().split("\r\n")
        self.array = [s for s in in_arr if s[0].isalnum()]

    async def hadle_array_command(self) -> bytes:

        command = self.array[0].upper()

        match command:
            case "PING":
                return await self.command_ping()
            case "SET":
                return await self.command_set()
            case "GET":
                return await self.command_get()
            case _:
                return await self.command_not_found()


    async def command_ping(self) -> bytes:
        return "+PONG\r\n".encode()

    async def command_set(self) -> bytes:
        
        if len(self.array) != 3:
            return self.return_error("SET command must have 3 parameters.")

        entry = Entry(key=self.array[1], value=self.array[2])
        await self.dicth.set(entry=entry)

        return "+OK\r\n".encode()

    async def command_get(self) -> bytes:

        if len(self.array)  != 2:
            return self.return_error("GET command must have 2 parameters.")

        value = await self.dicth.get(key=self.array[1]) 

        return self.construct_get_response(value=value)

    def construct_get_response(self, value: Any) -> bytes:
        return "$-1\r\n".encode() if value is None else  f"+{value}\r\n".encode()

    async def command_not_found(self) -> bytes:
        return "+NOT FOUND\r\n".encode()
    
    def return_error(self, err_message: str) -> bytes:
        return f"-{err_message}\r\n".encode()

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(data={self.data}, array={self.array})"

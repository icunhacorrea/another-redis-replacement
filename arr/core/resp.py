from arr.core.memory import Memory
from arr.request.array import ArrayRequest
from arr.utils.breader import ByteReader

class Resp:

    def __init__(self, mem: Memory) -> None:
        self.breader = ByteReader()
        self.mem = mem

    async def deserialize_request(self, data: bytes) -> bytes:

        first_b = data[0:1]

        match first_b:
            case b'*':
                req = ArrayRequest(self.mem, data)
                return await req.hadle_array_command()
            case _:
                return self.type_not_found()

    def type_not_found(self) -> bytes:
        return "+TYPE NOT FOUND\r\n".encode()


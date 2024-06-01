from arr.core.database.dicth import DictH
from arr.request.array import ArrayRequest
from arr.utils.breader import ByteReader

class Resp:

    def __init__(self, dicth: DictH) -> None:
        self.breader = ByteReader()
        self.dicth = dicth

    async def deserialize_request(self, data: bytes) -> bytes:

        first_b = data[0:1]

        match first_b:
            case b'*':
                req = ArrayRequest(self.dicth, data)
                return await req.hadle_array_command()
            case _:
                return self.type_not_found()

    def type_not_found(self) -> bytes:
        return "+TYPE NOT FOUND\r\n".encode()


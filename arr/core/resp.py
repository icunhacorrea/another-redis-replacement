from arr.utils.breader import ByteReader

class Resp:

    def __init__(self) -> None:
        self.breader = ByteReader()

    def decode_data(self, data: bytes) -> bytes | None:

        first_b = data[0:1]

        match first_b:
            case b'*':
                self.handle_array(data)
            case _:
                return self.command_not_found()

    def handle_array(self, bytearr: bytes) -> str:
        darray = bytearr.decode().strip().split("\r\n")
        print(darray)

    def handle_command(self, data: str) -> bytes | None:

        first_b = data[0:1]

        if first_b != b'*':
            print("Cant proceed")
            return None
        
        match data:
            case "PING":
                return self.command_ping()
            case _:
                return self.command_not_found()

        return None

    def command_ping(self) -> bytes:
        return "+PING\r\n".encode()

    def command_not_found(self) -> bytes:
        return "+NOT FOUND\r\n".encode()

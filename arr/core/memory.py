from typing import Any
from asyncio import Lock
from numba import jit

class Memory:

    def __init__(self) -> None:
        self._mem = {}
        self._lock = Lock()

    async def set(self, key: Any, value: Any):
        async with self._lock:
            self._mem[key] = value

    async def get(self, key: str) -> Any:
        if key not in self._mem.keys():
            return "*-1\r\n"
        return self._mem.get(key)

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(mem={self._mem})"


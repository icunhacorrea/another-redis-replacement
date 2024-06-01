from typing import Any
from asyncio import Lock
from arr.core.database.entry import Entry

class DictH:

    def __init__(self, max_size: int) -> None:
        self.max_size = max_size
        self.head = None
        self.entries = [None] * 128
        self._lock = Lock()

    async def set(self, entry: Entry):
        async with self._lock:

            bucket = self.radix_calculation(entry.key)
            print(f"Bucket: {bucket}")
            
            if self.entries[bucket] is None:
                self.entries[bucket] = entry
                return

            tmp = self.entries[bucket]

            while tmp is not None:
                if tmp.key == entry.key:
                    tmp.value = entry.value
                    return

                if tmp.next == None:
                    tmp.next = entry
                    return

                tmp = tmp.next
    
    async def get(self, key: str) -> Any | None:
        async with self._lock:

            bucket = self.radix_calculation(key)
            print(f"Bucket: {bucket}")

            if self.entries[bucket] is None:
                return None

            tmp = self.entries[bucket]

            while tmp is not None:
                if tmp.key == key:
                    return tmp.value
                tmp = tmp.next

            return None


    def radix_calculation(self, word: str) -> int:
        res = 0

        for i, letter in enumerate(word):
            res += (ord(letter) * (128 ^ i))

        return res % self.max_size

    def count_itens(self) -> int:
        count = 0
        tmp = self.head

        while tmp is not None:
            count += 1
            tmp = tmp.next

        return count

    def print_list(self) -> None:
        
        for i in range(len(self.entries)):
            print(f"Bucket: {i}")
            print("LIST -> ", end="")
            tmp = self.entries[i]
            while tmp is not None:
                print(f"(key={tmp.key}, value={tmp.value})", end=" -> ")
                tmp = tmp.next

            print(f"END {i}")
            print("=======================")

from asyncio import Lock
from arr.core.database.entry import Entry

class DictH:

    def __init__(self, max_size: int) -> None:
        self.max_size = max_size
        self.head = None
        self._lock = Lock()

    async def set(self, entry: Entry):
        async with self._lock:
            if self.head is None:
                self.head = entry
                return

            tmp = self.head

            while tmp is not None:
                if tmp.key == entry.key:
                    tmp.value = entry.value
                    return

                if tmp.next == None:
                    tmp.next = entry
                    return

                tmp = tmp.next
    
    async def get(self, key: str) -> Entry | None:
        tmp = self.head

        if key == tmp.key:
            return tmp

        while tmp is not None:
            if tmp.key == key:
                return tmp
            tmp = tmp.next

        return None


    def radix_calculation(self, word: str) -> int:
        res = 0

        for i, letter in enumerate(word):
            res += (ord(letter) * (128 ^ i))

        return res % self.max_size

    def print_list(self) -> int:
        tmp = self.head
        count = 0 

        while tmp is not None:
            count += 1
            print(tmp.key, tmp.value)
            tmp = tmp.next

        return count


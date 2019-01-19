class FakeDataGenerator:
    def __init__(self, total_bytes: int):
        self._count_bytes = 0
        self._total_bytes = total_bytes

    def read(self, b):
        if self._total_bytes == self._count_bytes:
            return b''

        if self._total_bytes >= (b + self._count_bytes):
            bytes_to_use = b
        else:
            bytes_to_use = self._total_bytes - self._count_bytes

        self._count_bytes += bytes_to_use

        return b'a' * bytes_to_use

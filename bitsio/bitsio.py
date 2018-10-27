"""
"""
from io import BytesIO


DEFAULT_BUFSIZE = 32


class BitsIO(object):
    """BitsIO
    """

    def __init__(self,
                 buf,
                 bitorder='msb',
                 byteorder='big',
                 bitbuf_size=DEFAULT_BUFSIZE):
        self.bytesio = BytesIO(buf)
        self.bitorder = bitorder
        self.byteorder = byteorder
        self.bitbuf = 0
        self.bitbuf_size = bitbuf_size
        self.left = self.bitbuf_size

    def read_bytes(self, size=1, byteorder='big'):
        return int.from_bytes(self.read(size), byteorder=byteorder)

    def read(self, size=1):
        if self.left == 8:
            self.value = self.read_bytes(1)
        left = self.left - size
        mask = (1 << size) - 1
        res = (self.value >> left) & mask
        self.left = 8 if left == 0 else left
        return res

    def read1(self):
        return 0

    def write(self, bits, size):
        ...

    def write1(self, bit):
        self.left -= 1

        if self.bitorder == 'msb':
            shift = self.left
        elif self.bitorder == 'lsb':
            shift = self.bitbuf_size - self.left - 1

        self.bitbuf |= bit << shift

        if self.left == 0:
            bytes = self.bitbuf
            self.bytesio.write(bytes)
            self.left = self.bitbuf_size

"""
"""
from io import BytesIO


DEFAULT_BUFSIZE = 32
OCTET = 8
BYTES_LENGTH = DEFAULT_BUFSIZE // OCTET


class BitsIO(object):
    """BitsIO
    """

    def __init__(self,
                 buf,
                 bitorder: str = 'msb',
                 byteorder: str = 'big'):
        self.bytesio = BytesIO(buf)
        if bitorder not in['msb', 'lsb']:
            raise ValueError("bitorder must be either 'msb' or 'lsb'")

        self.bitorder = bitorder
        self.byteorder = byteorder
        self.bitbuf_size = DEFAULT_BUFSIZE
        self._init_wbitbuf()
        self._init_rbitbuf()
        self.get_shift = {
            'msb': lambda left: left,
            'lsb': lambda left: DEFAULT_BUFSIZE - left - 1
        }

    def read(self, size: int):

        return 0

    def read1(self):
        self.rleft -= 1
        shift = self.get_shift[self.bitorder](self.rleft)
        bit = self.rbitbuf >> shift
        if self.rleft == 0:
            self._init_rbitbuf()
        return bit

    def _init_rbitbuf(self):
        self.rbitbuf = int.from_bytes(self.bytesio.read(
            BYTES_LENGTH), byteorder=self.byteorder)
        self.rleft = self.bitbuf_size

    def write(self, bits: int, size: int):
        ...

    def write1(self, bit: int):
        self.wleft -= 1
        shift = self.get_shift[self.bitorder](self.wleft)
        self.wbitbuf |= bit << shift

        if self.wleft == 0:
            bytes = self.wbitbuf.to_bytes(
                length=BYTES_LENGTH, byteorder=self.byteorder)
            self.bytesio.write(bytes)
            self._init_wbitbuf()

    def _init_wbitbuf(self):
        self.wbitbuf = 0
        self.wleft = self.bitbuf_size

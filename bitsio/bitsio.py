"""
"""
from io import BytesIO


DEFAULT_BUFSIZE = 32
OCTET = 8
BYTES_LENGTH = DEFAULT_BUFSIZE // OCTET
MSB = 'big'
LSB = 'little'
BYTE_ORDER_ERROR = "bitorder must be either '{0}' or '{1}'".format(MSB, LSB)


class BitsIO(object):
    """BitsIO
    """

    def __init__(self,
                 buf,
                 bitorder: str):
        self.bytesio = BytesIO(buf)
        if bitorder not in [MSB, LSB]:
            raise ValueError(BYTE_ORDER_ERROR)

        self.bitorder = bitorder
        self.byteorder = bitorder  # Byte order must be equal to bit order
        self.bitbuf_size = DEFAULT_BUFSIZE
        self._init_wbuf()
        self._init_rbuf()
        self.get_shift = {
            MSB: lambda left: left,
            LSB: lambda left: DEFAULT_BUFSIZE - left - 1
        }

    def read(self, size: int):

        return 0

    def read1(self):
        self.rleft -= 1
        shift = self.get_shift[self.bitorder](self.rleft)
        bit = (self.rbuf >> shift) & 1
        if self.rleft == 0:
            self._init_rbuf()
        return bit

    def _init_rbuf(self):
        self.rbuf = int.from_bytes(self.bytesio.read(
            BYTES_LENGTH), byteorder=self.byteorder)
        self.rleft = self.bitbuf_size

    def write1(self, bit: int):
        self.wleft -= 1
        shift = self.get_shift[self.bitorder](self.wleft)
        self.wbuf |= (bit & 1) << shift

        if self.wleft == 0:
            self._flush()

    def write(self, bits: int, size: int):
        l = size - self.wleft
        bits &= (1 << size) - 1
        # print('{:08b}'.format(bits))

        # msb first
        if l < 0:
            shift = -l
            self.wbuf |= bits << shift
            self.wleft = shift
        else:
            self.wbuf |= bits >> l
            self._flush()
            self.wleft = self.bitbuf_size - l

            if self.wleft < self.bitbuf_size:
                self.wbuf = bits << self.wleft

    def write_align(self):  # flash
        ...

    def _flush(self):
        bytes = self.wbuf.to_bytes(
            length=BYTES_LENGTH, byteorder=self.byteorder)
        #print('wbuf: {:032b}'.format(self.wbuf))
        #print('bytes:   {0}'.format(bytes))
        self.bytesio.write(bytes)
        self._init_wbuf()

    def _init_wbuf(self):
        self.wbuf = 0
        self.wleft = self.bitbuf_size

    def getvalue(self):
        return self.bytesio.getvalue()

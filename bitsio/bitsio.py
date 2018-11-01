"""
"""
from io import BytesIO


DEFAULT_BUFSIZE = 32
BUF_MASK = (1 << DEFAULT_BUFSIZE) - 1
OCTET = 8
NUM_BYTES = DEFAULT_BUFSIZE // OCTET
MSB = 'big'
LSB = 'little'
BYTE_ORDER_ERROR = "bitorder must be either '{0}' or '{1}'".format(MSB, LSB)


class BitsIO(object):
    """BitsIO
    TODO: Document
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
        """
        TODO: Document
        """
        # TODO: msb first
        # TODO: lsb first
        return 0

    def read1(self):
        """
        TODO: Document
        """
        self.rleft -= 1
        shift = self.get_shift[self.bitorder](self.rleft)
        bit = (self.rbuf >> shift) & 1
        if self.rleft == 0:
            self._init_rbuf()
        return bit

    def _init_rbuf(self):
        self.rbuf = int.from_bytes(self.bytesio.read(
            NUM_BYTES), byteorder=self.byteorder)
        self.rleft = self.bitbuf_size

    def write1(self, bit: int):
        """
        TODO: Document
        """
        self._write_bits(bit, 1)

        if self.wleft == 0:
            self._flush()

    def write(self, bits: int, size: int):
        """
        TODO: Document
        """
        # TODO: if size > bitbuf_size
        # msb first
        """
        left = self.wleft - size

        if left > 0:
            shift = self.get_shift[self.bitorder](left)
            self._write_bits(bits, shift)
            self.wleft = left
        else:
            shift = 0
            self._write_bits(bits >> (-left), shift)  # TODO: lsb first
            self._flush()
            self.wleft = self.bitbuf_size + left

            if self.wleft < self.bitbuf_size:
                shift = self.get_shift[self.bitorder](self.wleft)
                self._write_bits(bits, shift)
        return
        """
        # size = 10, wleft = 32, 10 - 32 = -22, 前半はなし。後半に10
        # size = 32, wleft = 32, 32 - 32 = 0, 前半に32。
        # size = 16, wleft = 10, 16 - 10 = 6: 10が前半、後半が6
        remainbits_size = size - self.wleft

        if remainbits_size >= 0:
            if self.bitorder == MSB:
                remainbits = bits >> remainbits_size
            elif self.bitorder == LSB:
                remainbits = bits & ((1 << self.wleft) - 1)
            self._write_bits(remainbits, self.wleft)
            self._flush()
            size = remainbits_size

        if size > 0:
            self._write_bits(bits, size)

    def write_align(self):  # flush
        """
        TODO: Document
        """
        ...

    def _write_bits(self, bits, size):
        bits &= (1 << size) - 1  # mask
        left = self.wleft - size
        # shift = self.get_shift[self.bitorder](left)
        if self.bitorder == MSB:
            shift = left
        elif self.bitorder == LSB:
            shift = DEFAULT_BUFSIZE - left - 1
        self.wbuf |= (bits << shift) & BUF_MASK
        self.wleft = left

    def _flush(self):
        # print('wbuf: {:032b}'.format(self.wbuf))
        bytes = self.wbuf.to_bytes(
            length=NUM_BYTES, byteorder=self.byteorder)
        # print('bytes:   {0}'.format(bytes))
        self.bytesio.write(bytes)
        self._init_wbuf()

    def _init_wbuf(self):
        self.wbuf = 0
        self.wleft = self.bitbuf_size

    def getvalue(self):
        """
        TODO: Document
        """
        return self.bytesio.getvalue()

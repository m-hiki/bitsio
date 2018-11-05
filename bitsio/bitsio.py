"""
"""
DEFAULT_BUFSIZE = 32
OCTET = 8
NUM_BYTES = DEFAULT_BUFSIZE // OCTET
MSB = 'big'
LSB = 'little'
REQUIRE_METHODS = {
    'read',
    'write',
    'tell',
    'seek'
}

IOOBJ_ERROR = "ioobj must be the class implementing {0}() method"
BYTE_ORDER_ERROR = "bitorder must be either '{0}' or '{1}'".format(MSB, LSB)


def mask(bits, size):
    return bits & ((1 << size) - 1)


class BitsIO(object):
    """BitsIO
    TODO: Document
    """

    def __init__(self,
                 ioobj,
                 bitorder: str):
        for method in REQUIRE_METHODS:
            if not hasattr(ioobj, method):
                raise ValueError(IOOBJ_ERROR.format(method))

        self.io = ioobj
        if bitorder not in [MSB, LSB]:
            raise ValueError(BYTE_ORDER_ERROR)

        self.bitorder = bitorder
        self.byteorder = bitorder  # Byte order must be equal to bit order
        self.bitbuf_size = DEFAULT_BUFSIZE
        self._init_buf()
        self.iopos = 0

    def read1(self):
        """
        TODO: Document
        """
        if self.left == self.bitbuf_size:
            self._load()

        bit = self._read_bits(1)
        return bit

    def read(self, size: int):
        """
        TODO: Document
        """
        latterbits_size = size - self.left
        bits = 0
        shift = 0

        if latterbits_size >= 0:
            shift = self.left
            firstbits = self._read_bits(self.left)
            if self.bitorder == MSB:
                bits = firstbits << latterbits_size
                shift = 0
            elif self.bitorder == LSB:
                bits = firstbits
            size = latterbits_size

        if self.left == self.bitbuf_size:
            self._load()

        if size > 0:
            bits |= self._read_bits(size) << shift
        return bits

    def _load(self):
        bytes = self.io.read(NUM_BYTES)
        self.buf = int.from_bytes(bytes, byteorder=self.byteorder)

    def _read_bits(self, size):
        shift = self._get_shift(size)
        bit = mask(self.buf >> shift, size)
        self.left -= size

        if self.left == 0:
            self._init_buf()
        return bit

    def write1(self, bit: int):
        """
        param bit
        Write 1 bit to buffer
        """
        self._write_bits(bit, 1)

        if self.left == 0:
            self._flush()

    def write(self, bits: int, size: int):
        """
        param bits
        Write bits of size to buffer
        """
        # TODO: if size > bitbuf_size
        latterbits_size = size - self.left

        if latterbits_size >= 0:
            if self.bitorder == MSB:
                firstbits = bits >> latterbits_size
            elif self.bitorder == LSB:
                firstbits = bits
                bits = bits >> latterbits_size
            self._write_bits(firstbits, self.left)
            self._flush()
            size = latterbits_size

        if size > 0:
            self._write_bits(bits, size)

    def write_align(self):
        """
        Write alignment bits of 0s and flush.
        """
        self._write_bits(0, self.left)
        self._flush()

    def _write_bits(self, bits, size):
        bits = mask(bits, size)
        shift = self._get_shift(size)
        self.buf |= mask(bits << shift, self.bitbuf_size)
        self.left -= size

    def _flush(self):
        # print('wbuf: {:032b}'.format(self.buf))
        bytes = self.buf.to_bytes(length=NUM_BYTES, byteorder=self.byteorder)
        # print('bytes:   {0}'.format(bytes))
        self.io.write(bytes)
        self._init_buf()

    def _init_buf(self):
        self.buf = 0
        self.left = self.bitbuf_size
        self.iopos = self.io.tell()

    def _get_shift(self, size):
        if self.bitorder == MSB:
            shift = self.left - size
        elif self.bitorder == LSB:
            shift = self.bitbuf_size - self.left
        return shift

    def tell(self):
        """
        Current position in bit stream, an integer.
        """
        bits = self.bitbuf_size - self.left
        return self.iopos * OCTET + bits

    def seek(self, pos):
        """
        param pos

        Change stream position.
        """
        # TODO: implement
        bytes_pos = 0
        self.io.seek(bytes_pos)

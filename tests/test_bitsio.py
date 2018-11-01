import unittest
from bitsio import BitsIO


class TestBitsIO(unittest.TestCase):
    def setUp(self):
        self.WRITE_TEST_INPUT = bytearray([1, 2, 3, 4, 5, 6, 7, 8])
        # t = 0b0001_0010_0011_0100_0101_0110

    def test_init(self):
        exception = None

        try:
            BitsIO(b'', bitorder='NotMsbOrLsb')
        except Exception as e:
            exception = e

        self.assertEqual(ValueError, exception.__class__)

    def test_write1_msb_first(self):
        bitsio = BitsIO(b'',  bitorder='big')
        for byte in self.WRITE_TEST_INPUT:
            for n in range(0, 8):
                shift = 7 - n
                bit = (byte >> shift) & 1
                bitsio.write1(bit)

        actual_bytebuf = bitsio.getvalue()
        self.assertEqual(self.WRITE_TEST_INPUT, actual_bytebuf)

    def test_write1_lsb_first(self):
        bitsio = BitsIO(b'', bitorder='little')
        for byte in self.WRITE_TEST_INPUT:
            for n in range(0, 8):
                shift = n
                bit = (byte >> shift) & 1
                bitsio.write1(bit)

        actual_bytebuf = bitsio.getvalue()
        self.assertEqual(self.WRITE_TEST_INPUT, actual_bytebuf)

    def test_write_msb_first(self):
        bitsio = BitsIO(b'', bitorder='big')
        input = self.WRITE_TEST_INPUT[0]
        bitsio.write(input, 8)  # left: 24
        input = (self.WRITE_TEST_INPUT[1] << 8) | self.WRITE_TEST_INPUT[2]
        bitsio.write(input, 16)  # left: 8
        input = (self.WRITE_TEST_INPUT[3] << 16) | \
            (self.WRITE_TEST_INPUT[4] << 8) | self.WRITE_TEST_INPUT[5]
        bitsio.write(input, 24)  # 1 flush, left: 16
        input = (self.WRITE_TEST_INPUT[6] << 8) | self.WRITE_TEST_INPUT[7]
        bitsio.write(input, 16)  # 1 flush

        actual_bytebuf = bitsio.getvalue()
        self.assertEqual(self.WRITE_TEST_INPUT, actual_bytebuf)

    def test_write_lsb_first(self):
        bitsio = BitsIO(b'', bitorder='little')
        input = self.WRITE_TEST_INPUT[3]
        bitsio.write(input, 8)  # left: 24
        input = (self.WRITE_TEST_INPUT[2] << 8) | self.WRITE_TEST_INPUT[1]
        bitsio.write(input, 16)  # left: 8
        input = (self.WRITE_TEST_INPUT[0] << 16) | \
            (self.WRITE_TEST_INPUT[7] << 8) | self.WRITE_TEST_INPUT[6]
        #print('input: {0:b}'.format(input))
        bitsio.write(input, 24)  # 1 flush, left: 16
        input = (self.WRITE_TEST_INPUT[5] << 8) | self.WRITE_TEST_INPUT[4]
        bitsio.write(input, 16)  # 1 flush

        actual_bytebuf = bitsio.getvalue()
        self.assertEqual(self.WRITE_TEST_INPUT, actual_bytebuf)


if __name__ == '__main__':
    unittest.main()

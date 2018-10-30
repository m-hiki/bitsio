import unittest
from bitsio import BitsIO


class TestBitsIO(unittest.TestCase):
    def setUp(self):
        self.WRITE1_TEST_INPUT = bytearray([1, 2, 3, 4, 5, 6, 7, 8])
        #t = 0b0001_0010_0011_0100_0101_0110

    def test_init(self):
        exception = None

        try:
            BitsIO(b'', bitorder='NotMsbOrLsb')
        except Exception as e:
            exception = e

        self.assertEqual(ValueError, exception.__class__)

    def test_write1_msb_first(self):
        bitsio = BitsIO(b'',  bitorder='big')
        for byte in self.WRITE1_TEST_INPUT:
            for n in range(0, 8):
                shift = 7 - n
                bit = (byte >> shift) & 1
                bitsio.write1(bit)

        actual_bytebuf = bitsio.getvalue()
        self.assertEqual(self.WRITE1_TEST_INPUT, actual_bytebuf)

    def test_write1_lsb_first(self):
        bitsio = BitsIO(b'', bitorder='little')
        for byte in self.WRITE1_TEST_INPUT:
            for n in range(0, 8):
                shift = n
                bit = (byte >> shift) & 1
                bitsio.write1(bit)

        actual_bytebuf = bitsio.getvalue()
        self.assertEqual(self.WRITE1_TEST_INPUT, actual_bytebuf)

    def test_write_msb_first(self):
        bitsio = BitsIO(b'',  bitorder='big')
        bitsio.write(0x01, 8)
        bitsio.write(0x02, 8)
        bitsio.write(0x03, 8)
        bitsio.write(0x04, 8)
        print(bitsio.getvalue())

    def test_write_lsb_first(self):
        bitsio = BitsIO(b'', bitorder='little')


if __name__ == '__main__':
    unittest.main()

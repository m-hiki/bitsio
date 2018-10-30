import unittest
from bitsio import BitsIO


class TestBitsIO(unittest.TestCase):
    def setUp(self):
        self.WRITE_TEST_INPUT = bytearray([1, 2, 3, 4, 5, 6, 7, 8])

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

        actual_bytebuf = bitsio.bytesio.getvalue()
        self.assertEqual(self.WRITE_TEST_INPUT, actual_bytebuf)

    def test_write1_lsb_first(self):
        bitsio = BitsIO(b'', bitorder='little')
        for byte in self.WRITE_TEST_INPUT:
            for n in range(0, 8):
                shift = n
                bit = (byte >> shift) & 1
                bitsio.write1(bit)

        actual_bytebuf = bitsio.bytesio.getvalue()
        self.assertEqual(self.WRITE_TEST_INPUT, actual_bytebuf)


if __name__ == '__main__':
    unittest.main()

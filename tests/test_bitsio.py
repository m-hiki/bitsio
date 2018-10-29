import unittest
from bitsio import BitsIO


class TestBitsIO(unittest.TestCase):
    """
    msb first, big endian
    msb first, little endian
    lsb first, big endian
    lsb first, little endian
    """

    def setUp(self):
        self.WRITE_TEST_INPUT = bytearray([1, 2, 3, 4, 5, 6, 7, 8])

    def test_init(self):
        exception = None

        try:
            BitsIO(b'', bitorder='NotMsbOrLsb')
        except Exception as e:
            exception = e

        self.assertEqual(ValueError, exception.__class__)

    def test_write1_msb_big(self):
        bitsio = BitsIO(b'')
        for byte in self.WRITE_TEST_INPUT:
            for n in range(0, 8):
                shift = 7 - n
                bit = byte >> shift & 1
                bitsio.write1(bit)
                # self.assertEqual(actual, expected)

        actual_bytebuf = bitsio.bytesio.getvalue()
        self.assertEqual(self.WRITE_TEST_INPUT, actual_bytebuf)

    def test_write1_msb_little(self):
        bitsio = BitsIO(b'', byteorder='little')
        expected_bytebuf = bytearray([4, 3, 2, 1, 8, 7, 6, 5])
        for byte in self.WRITE_TEST_INPUT:
            for n in range(0, 8):
                shift = 7 - n
                bit = byte >> shift & 1
                bitsio.write1(bit)
                # self.assertEqual(actual, expected)

        actual_bytebuf = bitsio.bytesio.getvalue()
        self.assertEqual(expected_bytebuf, actual_bytebuf)
        self.assertTrue(False)

    def test_write1_lsb_big(self):
        self.assertTrue(False)

    def test_write1_lsb_little(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()

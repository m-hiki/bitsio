# Copyright 2018 Minoru Hiki
# License: MIT, see LICENSE for more detail
import unittest
from io import BytesIO
from bitsio import BitsIO
from random import randint


TEST_BYTES = bytearray([1, 2, 3, 4, 5, 6, 7, 8])
TEST_BITS = {
    'big':
        '0000000100000010000000110000010000000101000001100000011100001000',
    'little':
        '1000000001000000110000000010000010100000011000001110000000010000',
}
TEST_POS = [
    {'pos': 14, 'bit': 1},
    {'pos': 14, 'bit': 1},
]


class TestBitsIO(unittest.TestCase):

    def test_init(self):
        exception = None

        try:
            BitsIO(BytesIO(b''), bitorder='NotMsbOrLsb')
        except Exception as e:
            exception = e

        self.assertEqual(ValueError, exception.__class__)

    def _test_rea1(self, endian):
        bytesio = BytesIO(TEST_BYTES)
        bitsio = BitsIO(bytesio, bitorder=endian)
        expected_bits = TEST_BITS[endian]

        for expected_pos, expected_bit in enumerate(expected_bits):
            actual_pos = bitsio.tell()
            self.assertEqual(expected_pos, actual_pos)
            actual_bit = bitsio.read1()
            self.assertEqual(int(expected_bit), actual_bit)

        pos = bitsio.tell()
        self.assertEqual(len(expected_bits), pos)

    def test_read1(self):
        self._test_rea1('big')
        self._test_rea1('little')

    def _test_read(self, endian):
        bytesio = BytesIO(TEST_BYTES)
        bitsio = BitsIO(bytesio, bitorder=endian)
        sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9]
        expected_pos = 0

        for size in sizes:
            sbits = TEST_BITS[endian][expected_pos:expected_pos + size]
            if endian == 'little':
                sbits = sbits[::-1]
            expected_bits = int(sbits, 2)
            actual_bits = bitsio.read(size)
            self.assertEqual(expected_bits, actual_bits)
            expected_pos += size
            actual_pos = bitsio.tell()
            self.assertEqual(expected_pos, actual_pos)

    def test_read(self):
        self._test_read('big')
        self._test_read('little')

    def _test_write1(self, endian):
        bytesio = BytesIO(b'')
        bitsio = BitsIO(bytesio, bitorder=endian)
        input = TEST_BITS[endian]

        for expected_pos, bit in enumerate(input):
            actual_pos = bitsio.tell()
            self.assertEqual(expected_pos, actual_pos)
            bitsio.write1(int(bit, 2))

        actual_values = bytesio.getvalue()
        self.assertEqual(TEST_BYTES, actual_values)
        pos = bitsio.tell()
        self.assertEqual(len(input), pos)

    def test_write1(self):
        self._test_write1('big')
        self._test_write1('little')

    def _test_write(self, endian):
        bytesio = BytesIO(b'')
        bitsio = BitsIO(bytesio, bitorder=endian)
        sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9]
        expected_pos = 0

        for size in sizes:
            sbits = TEST_BITS[endian][expected_pos:expected_pos + size]
            if endian == 'little':
                sbits = sbits[::-1]
            bits = int(sbits, 2)
            bitsio.write(bits, size)
            expected_pos += size
            actual_pos = bitsio.tell()
            self.assertEqual(expected_pos, actual_pos)

        actual_bytebuf = bytesio.getvalue()
        self.assertEqual(TEST_BYTES, actual_bytebuf)

    def test_write(self):
        self._test_write('big')
        self._test_write('little')

    def _test_seek(self, endian):
        bytesio = BytesIO(TEST_BYTES)
        bitsio = BitsIO(bytesio, bitorder=endian)
        for _ in range(1, 100):
            expected_pos = randint(0, 31)
            expected_bit = int(TEST_BITS[endian][expected_pos])
            bitsio.seek(expected_pos)
            actual_pos = bitsio.tell()
            self.assertEqual(expected_pos, actual_pos)
            actual_bit = bitsio.read1()
            self.assertEqual(expected_bit, actual_bit)

    def test_seek(self):
        self._test_seek('big')
        self._test_seek('little')


if __name__ == '__main__':
    unittest.main()

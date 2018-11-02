import unittest
from bitsio import BitsIO


TEST_BYTES = bytearray([1, 2, 3, 4, 5, 6, 7, 8])
TEST_BITS = {
    'big': '0000000100000010000000110000010000000101000001100000011100001000',
    'little': '1000000001000000110000000010000010100000011000001110000000010000',
}


class TestBitsIO(unittest.TestCase):

    def test_init(self):
        exception = None

        try:
            BitsIO(b'', bitorder='NotMsbOrLsb')
        except Exception as e:
            exception = e

        self.assertEqual(ValueError, exception.__class__)

    def _test_rea1(self, endian):
        bitsio = BitsIO(TEST_BYTES, bitorder=endian)
        expected_bits = TEST_BITS[endian]

        for expected_pos, expected_bit in enumerate(expected_bits):
            actual_pos = bitsio.tell()
            self.assertEqual(expected_pos, actual_pos)
            actual_bit = bitsio.read1()
            self.assertEqual(int(expected_bit), actual_bit)

        pos = bitsio.tell()
        self.assertEqual(len(expected_bit), pos)

    def test_read1(self):
        # self._test_rea1('big')
        # self._test_rea1('little')
        ...

    def _test_read(self, endian):
        ...

    def test_read(self):
        # self._test_read('big')
        # self._test_rea1('little')
        ...

    def _test_write1(self, endian):
        bitsio = BitsIO(b'', bitorder=endian)
        input = TEST_BITS[endian]

        for expected_pos, bit in enumerate(input):
            actual_pos = bitsio.tell()
            self.assertEqual(expected_pos, actual_pos)
            bitsio.write1(int(bit, 2))

        actual_values = bitsio.getvalue()
        self.assertEqual(TEST_BYTES, actual_values)
        pos = bitsio.tell()
        self.assertEqual(len(input), pos)

    def test_write1(self):
        self._test_write1('big')
        self._test_write1('little')

    def _test_write(self, endian):
        bitsio = BitsIO(b'', bitorder=endian)
        sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9]
        expected_pos = 0

        for size in sizes:
            sbits = TEST_BITS[endian][expected_pos:expected_pos + size]
            if endian == 'little':
                sbits = sbits[::-1]
            bits = int(sbits, 2)
            bitsio.write(bits, size)
            expected_pos += size

        actual_bytebuf = bitsio.getvalue()
        self.assertEqual(TEST_BYTES, actual_bytebuf)

    def test_write(self):
        self._test_write('big')
        self._test_write('little')


if __name__ == '__main__':
    unittest.main()

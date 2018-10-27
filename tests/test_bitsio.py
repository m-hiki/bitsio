import unittest
from bitsio import BitsIO


class TestBitsIO(unittest.TestCase):
    """Basic test cases."""

    def test_read1_001(self):
        bitsio = BitsIO(b'')
        bitsio.write1(1)
        actual = bitsio.bitbuf
        expected = 1
        self.assertEqual(actual, expected)
        bitsio.write1(1)
        actual = bitsio.bitbuf
        expected = 3
        self.assertEqual(actual, expected)

    def test_read1_002(self):
        bitsio = BitsIO(b'', bitorder='lsb')
        bitsio.write1(1)
        actual = bitsio.bitbuf
        expected = 1
        self.assertEqual(actual, expected)
        bitsio.write1(1)
        actual = bitsio.bitbuf
        expected = 3
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()

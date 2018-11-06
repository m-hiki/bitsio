
from bitsio import BitsIO


def main():
    test_input = 'TEST'

    with open('test.txt', 'wb') as f:
        bitsio = BitsIO(f, bitorder='big')
        for s in test_input:
            bitsio.write(ord(s), 8)


if __name__ == '__main__':
    main()

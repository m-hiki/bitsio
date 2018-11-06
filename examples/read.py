
from io import BytesIO
from bitsio import BitsIO


def main():
    bytesio = BytesIO(b'HELLO')
    bitsio = BitsIO(bytesio, bitorder='big')
    for _ in range(1, 6):
        print(chr(bitsio.read(8)))


if __name__ == '__main__':
    main()

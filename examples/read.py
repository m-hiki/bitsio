
from io import BytesIO
from bitsio import BitsIO


def main():
    bytesio = BytesIO(b'TEST')
    bitsio = BitsIO(bytesio, bitorder='big')
    for _ in range(1, 5):
        print(chr(bitsio.read(8)))


if __name__ == '__main__':
    main()

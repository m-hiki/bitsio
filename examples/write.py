
from bitsio import BitsIO


def main():
    test_input = 'TEST'
    bitsio = BitsIO(b'', bitorder='big')
    for s in test_input:
        bitsio.write(ord(s), 8)

    with open('test.txt', 'wb') as f:
        f.write(bitsio.getvalue())


if __name__ == '__main__':
    main()

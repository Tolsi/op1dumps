#!/usr/bin/env python3
import itertools

column_parity_table = [
    0x00, 0x55, 0x59, 0x0c, 0x65, 0x30, 0x3c, 0x69,
    0x69, 0x3c, 0x30, 0x65, 0x0c, 0x59, 0x55, 0x00,
    0x95, 0xc0, 0xcc, 0x99, 0xf0, 0xa5, 0xa9, 0xfc,
    0xfc, 0xa9, 0xa5, 0xf0, 0x99, 0xcc, 0xc0, 0x95,
    0x99, 0xcc, 0xc0, 0x95, 0xfc, 0xa9, 0xa5, 0xf0,
    0xf0, 0xa5, 0xa9, 0xfc, 0x95, 0xc0, 0xcc, 0x99,
    0x0c, 0x59, 0x55, 0x00, 0x69, 0x3c, 0x30, 0x65,
    0x65, 0x30, 0x3c, 0x69, 0x00, 0x55, 0x59, 0x0c,
    0xa5, 0xf0, 0xfc, 0xa9, 0xc0, 0x95, 0x99, 0xcc,
    0xcc, 0x99, 0x95, 0xc0, 0xa9, 0xfc, 0xf0, 0xa5,
    0x30, 0x65, 0x69, 0x3c, 0x55, 0x00, 0x0c, 0x59,
    0x59, 0x0c, 0x00, 0x55, 0x3c, 0x69, 0x65, 0x30,
    0x3c, 0x69, 0x65, 0x30, 0x59, 0x0c, 0x00, 0x55,
    0x55, 0x00, 0x0c, 0x59, 0x30, 0x65, 0x69, 0x3c,
    0xa9, 0xfc, 0xf0, 0xa5, 0xcc, 0x99, 0x95, 0xc0,
    0xc0, 0x95, 0x99, 0xcc, 0xa5, 0xf0, 0xfc, 0xa9,
    0xa9, 0xfc, 0xf0, 0xa5, 0xcc, 0x99, 0x95, 0xc0,
    0xc0, 0x95, 0x99, 0xcc, 0xa5, 0xf0, 0xfc, 0xa9,
    0x3c, 0x69, 0x65, 0x30, 0x59, 0x0c, 0x00, 0x55,
    0x55, 0x00, 0x0c, 0x59, 0x30, 0x65, 0x69, 0x3c,
    0x30, 0x65, 0x69, 0x3c, 0x55, 0x00, 0x0c, 0x59,
    0x59, 0x0c, 0x00, 0x55, 0x3c, 0x69, 0x65, 0x30,
    0xa5, 0xf0, 0xfc, 0xa9, 0xc0, 0x95, 0x99, 0xcc,
    0xcc, 0x99, 0x95, 0xc0, 0xa9, 0xfc, 0xf0, 0xa5,
    0x0c, 0x59, 0x55, 0x00, 0x69, 0x3c, 0x30, 0x65,
    0x65, 0x30, 0x3c, 0x69, 0x00, 0x55, 0x59, 0x0c,
    0x99, 0xcc, 0xc0, 0x95, 0xfc, 0xa9, 0xa5, 0xf0,
    0xf0, 0xa5, 0xa9, 0xfc, 0x95, 0xc0, 0xcc, 0x99,
    0x95, 0xc0, 0xcc, 0x99, 0xf0, 0xa5, 0xa9, 0xfc,
    0xfc, 0xa9, 0xa5, 0xf0, 0x99, 0xcc, 0xc0, 0x95,
    0x00, 0x55, 0x59, 0x0c, 0x65, 0x30, 0x3c, 0x69,
    0x69, 0x3c, 0x30, 0x65, 0x0c, 0x59, 0x55, 0x00,
]

def crc(data):
    col_parity = 0
    line_parity = 0
    line_parity_prime = 0
    t=0
    b=0

    for i in range(0, 256):
        b = column_parity_table[data[i]]
        col_parity ^= b;

        if (b & 0x01): #	/* odd number of bits in the byte */
            line_parity ^= i
            line_parity_prime ^= ~i

    ecc = [0,0,0]
    ecc[2] = (~col_parity) | 0x03;

    t = 0;
    if (line_parity & 0x80):
        t |= 0x80;
    if (line_parity_prime & 0x80):
        t |= 0x40;
    if (line_parity & 0x40):
        t |= 0x20;
    if (line_parity_prime & 0x40):
        t |= 0x10;
    if (line_parity & 0x20):
        t |= 0x08;
    if (line_parity_prime & 0x20):
        t |= 0x04;
    if (line_parity & 0x10):
        t |= 0x02;
    if (line_parity_prime & 0x10):
        t |= 0x01;
    ecc[1] = ~t;

    t = 0;
    if (line_parity & 0x08):
        t |= 0x80;
    if (line_parity_prime & 0x08):
        t |= 0x40;
    if (line_parity & 0x04):
        t |= 0x20;
    if (line_parity_prime & 0x04):
        t |= 0x10;
    if (line_parity & 0x02):
        t |= 0x08;
    if (line_parity_prime & 0x02):
        t |= 0x04;
    if (line_parity & 0x01):
        t |= 0x02;
    if (line_parity_prime & 0x01):
        t |= 0x01;
    ecc[0] = ~t;

    return ecc

if __name__ == '__main__':
    data = bytes.fromhex("""06 50 5F AD 00 00 A0 FF 00 00 00 00 F0 0B 00 00
06 00 28 AD 00 40 80 FF BC 00 00 00 00 00 00 00
00 00 00 00 00 FF FF 03 00 01 02 03 04 05 06 07
08 09 0A 00 01 02 03 04 05 06 07 08 09 0A 0C 0D
0E 0F 10 11 12 13 14 15 20 03 23 00 00 08 00 CF
EF D0 C0 CB 00 80 80 80 80 60 F0 FF 0F 0F FF FF
FF FF 60 FF FF FF FF FF FF 20 3F 00 FF FF 3F 00
00 00 00 00 01 00 00 00 02 00 00 00 03 00 00 00
04 00 00 00 05 00 00 00 05 00 00 00 06 00 00 00
07 00 00 00 00 00 00 00 01 00 00 00 02 00 00 00
03 00 00 00 04 00 00 00 04 00 00 00 05 00 00 00
04 00 00 00 05 00 00 00 06 00 00 00 07 00 00 00
07 00 00 00 03 3F 01 00 10 74 03 00 50 87 54 14
00 60 00 FF 00 FF 00 00 00 00 00 00 06 00 31 AD
00 00 A0 FF CC 09 00 00 00 00 00 00 00 E8 04 00
E3 05 A6 6F 04 CC 2D 4A B8 B0 00 00 2B E1 64 01""")
    # should be D6 4D D1
    print('Flash block ECC:')
    print('hex:\t' + ''.join(map(str, crc(data))))
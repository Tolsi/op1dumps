#!/usr/bin/env python3
import itertools

# By https://www.micron.com/-/media/client/global/documents/products/technical-note/nand-flash/tn2963_ecc_in_slc_nand.pdf
def crc(data):
    LP17 = 0
    LP16 = 0
    LP15 = 0
    LP14 = 0
    LP13 = 0
    LP12 = 0
    LP11 = 0
    LP10 = 0
    LP9 = 0
    LP8 = 0
    LP7 = 0
    LP6 = 0
    LP5 = 0
    LP4 = 0
    LP3 = 0
    LP2 = 0
    LP1 = 0
    LP0 = 0

    CP5 = 0
    CP4 = 0
    CP3 = 0
    CP2 = 0
    CP1 = 0
    CP0 = 0

    for i in range(0, len(data)):
        bits = format(data[i], '08b')
        bit0 = int(bits[7], 2)
        bit1 = int(bits[6], 2)
        bit2 = int(bits[5], 2)
        bit3 = int(bits[4], 2)
        bit4 = int(bits[3], 2)
        bit5 = int(bits[2], 2)
        bit6 = int(bits[1], 2)
        bit7 = int(bits[0], 2)
        line = bit7 ^ bit6 ^ bit5 ^ bit4 ^ bit3 ^ bit2 ^ bit1 ^ bit0

        if (i & 0x01):
            LP1 = line ^ LP1
        else:
            LP0 = line ^ LP0

        if (i & 0x02):
            LP3 = line ^ LP3
        else:
            LP2 = line ^ LP2

        if (i & 0x04):
            LP5 = line ^ LP5
        else:
            LP4 = line ^ LP4

        if (i & 0x08):
            LP7 = line ^ LP7
        else:
            LP6 = line ^ LP6

        if (i & 0x10):
            LP9 = line ^ LP9
        else:
            LP8 = line ^ LP8

        if (i & 0x20):
            LP11 = line ^ LP11
        else:
            LP10 = line ^ LP10

        if (i & 0x40):
            LP13 = line ^ LP13
        else:
            LP12 = line ^ LP12

        if (i & 0x80):
            LP15 = line ^ LP15
        else:
            LP14 = line ^ LP14

        if (i & 0xA0):
            LP17 = line ^ LP17
        else:
            LP16 = line ^ LP16

        CP0 = bit6 ^ bit4 ^ bit2 ^ bit0 ^ CP0
        CP1 = bit7 ^ bit5 ^ bit3 ^ bit1 ^ CP1
        CP2 = bit5 ^ bit4 ^ bit1 ^ bit0 ^ CP2
        CP3 = bit7 ^ bit6 ^ bit3 ^ bit2 ^ CP3
        CP4 = bit3 ^ bit2 ^ bit1 ^ bit0 ^ CP4
        CP5 = bit7 ^ bit6 ^ bit5 ^ bit4 ^ CP5

    Ecc0 = [LP7, LP6, LP5, LP4, LP3, LP2, LP1, LP0]
    Ecc1 = [LP15, LP14, LP13, LP12, LP11, LP10, LP9, LP8]
    Ecc2 = [LP17, LP16, CP0, CP1, CP2, CP3, CP4, CP5]
    return list(itertools.chain.from_iterable([Ecc0, Ecc1, Ecc2]))

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
E3 05 A6 6F 04 CC 2D 4A B8 B0 00 00 2B E1 64 01
4B E1 C0 FF 04 CC 24 48 1D 93 00 00 0F 60 2C E1
24 01 4C E1 C0 FF 27 93 00 E3 F6 02 29 E1 08 32
49 E1 C0 FF 48 95 40 4C 09 8A 28 E1 30 17 48 E1
C0 FF 41 95 41 4A 40 8A 26 E1 00 01 2A E1 08 17
4A E1 C0 FF 92 8B 0D E1 04 40 4D E1 80 FF 69 91
1A 60 20 E1 D0 00 0D 9B 69 91 8D E6 01 00 69 91
8D E6 02 00 69 91 8D E6 03 00 69 91 4D B0 8D B0
8A B5 81 6C 49 30 0D 92 0D 92 0D 93 4D B0 8D B0
CD B0 0D B1 51 30 00 E3 3D 02 69 91 89 A1 CA A1
C9 B1 8A B1 09 A1 4A A1 49 B1 0A B1 00 E3 70 02
00 E3 F2 02 D0 60 00 E3 F7 03 00 0C 00 02 08 E1
00 40 48 E1 80 FF 00 9B 00 E3 8A 00 00 E3 32 01
00 E3 02 01 00 E3 5E 00 00 E3 A8 01 4F 30 C1 67
11 30 30 30 C1 67 20 E1 D8 00 00 E3 13 02 00 0C
0C 18 B0 A2 F1 A2 08 56 00 0C 0C 60 06 10 30 A3
71 A3 08 56 08 02 04 02 B9 AC 0C 0C 89 AE 03 10
D1 FF FF FF FF FF
""")
    b = ''.join(map(str, crc(data)))
    h = hex(int(b, 2))
    print('Flash block ECC:')
    print('Result (hex):\t' + h)

    res = crc(data)
    if h == '0x78c7fb':
        print('Found!')
    else:
        print(':<')

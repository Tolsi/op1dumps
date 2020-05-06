#!/usr/bin/env python3
import binascii
import itertools

# NOTE: the blackfin is a little endian system, so the ECC has to be swapped to match the values
#       from a flash dump. Also it seems that the "rest" of the value is filled with 1 (padded)

def getbytes(bits):
    done = False
    while not done:
        byte = 0
        for _ in range(0, 8):
            try:
                bit = next(bits)
            except StopIteration:
                bit = 0
                done = True
            byte = (byte << 1) | bit
        yield byte

# crude test implementation of BF5xx ECC code
# returns 3 bytes ECC in little endian
def crc(data):
    P1 = 0
    P2 = 0
    P4 = 0
    P8 = 0
    P16 = 0
    P32 = 0
    P64 = 0
    P128 = 0
    P256 = 0
    P512 = 0
    P1024 = 0
    P1_1 = 0
    P2_1 = 0
    P4_1 = 0
    P8_1 = 0
    P16_1 = 0
    P32_1 = 0
    P64_1 = 0
    P128_1 = 0
    P256_1 = 0
    P512_1 = 0
    P1024_1 = 0

    counter16 = 0
    counting16odd = False
    counter32 = 0
    counting32odd = False
    counter64 = 0
    counting64odd = False
    counter128 = 0
    counting128odd = False
    counter256 = 0
    counting256odd = False
    counter512 = 0
    counting512odd = False
    counter1024 = 0
    counting1024odd = False

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

        # P1 takes ALL odd bits XOR, P1_1 all even bits
        P1   = P1   ^ bit1 ^ bit3 ^ bit5 ^ bit7
        P1_1 = P1_1 ^ bit0 ^ bit2 ^ bit4 ^ bit6
        # P2 takes bits 2,3 and 6,7, P2_1 takes 0,1 and 4,5 (2bits sequence)
        P2   = P2   ^ bit2 ^ bit3 ^ bit6 ^ bit7
        P2_1 = P2_1 ^ bit0 ^ bit1 ^ bit4 ^ bit5
        # P4 takes 4,5,6,7, P4_1 takes 0,1,2,3  (4bits sequence)
        P4   = P4   ^ bit4 ^ bit5 ^ bit6 ^ bit7
        P4_1 = P4_1 ^ bit0 ^ bit1 ^ bit2 ^ bit3
        # P8 takes all 8 bits from odd Bytecount, P8_1 all 8 bits from even Bytecount
        if (i % 2) != 0:
            P8   = P8   ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
        else:
            P8_1 = P8_1 ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
        # P16 takes 16 bit from odd Bytecount, P16_1 takes 16 bits from even Bytecounts
        if counting16odd == True:
            counter16 += 1
            P16  = P16  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter16 == 2:
                counting16odd = False
                counter16=0
        else:
            counter16 += 1
            P16_1  = P16_1  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter16 == 2:
                counting16odd = True
                counter16=0
        # P32 takes 32 bit from odd Bytecount, P32_1 takes 32 bits from even Bytecounts
        if counting32odd:
            counter32 += 1
            P32  = P32  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter32 == 4:
                counting32odd = False
                counter32=0
        else:
            counter32 += 1
            P32_1  = P32_1  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter32 == 4:
                counting32odd = True
                counter32=0
        # P64 takes 64 bit from odd Bytecount, P64_1 takes 64 bits from even Bytecounts
        if counting64odd:
            counter64 += 1
            P64  = P64  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter64 == 8:
                counting64odd = False
                counter64=0
        else:
            counter64 += 1
            P64_1  = P64_1  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter64 == 8:
                counting64odd = True
                counter64=0
        # P128 takes 128 bit from odd Bytecount, P128_1 takes 128 bits from even Bytecounts
        if counting128odd:
            counter128 += 1
            P128  = P128  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter128 == 16:
                counting128odd = False
                counter128=0
        else:
            counter128 += 1
            P128_1  = P128_1  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter128 == 16:
                counting128odd = True
                counter128=0
        # P256 takes 256 bit from odd Bytecount, P256_1 takes 256 bits from even Bytecounts
        if counting256odd:
            counter256 += 1
            P256  = P256  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter256 == 32:
                counting256odd = False
                counter256=0
        else:
            counter256 += 1
            P256_1  = P256_1  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter256 == 32:
                counting256odd = True
                counter256=0
        # P512 takes 512 bit from odd Bytecount, P512_1 takes 512 bits from even Bytecounts
        if counting512odd:
            counter512 += 1
            P512  = P512  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter512 == 64:
                counting512odd = False
                counter512=0
        else:
            counter512 += 1
            P512_1  = P512_1  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter512 == 64:
                counting512odd = True
                counter512=0
        # P1024 takes 1024 bit from odd Bytecount, P1024_1 takes 1024 bits from even Bytecounts
        if counting1024odd:
            counter1024 += 1
            P1024  = P1024  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter1024 == 128:
                counting1024odd = False
                counter1024=0
        else:
            counter1024 += 1
            P1024_1  = P1024_1  ^ bit0 ^ bit1 ^ bit2 ^ bit3 ^ bit4 ^ bit5 ^ bit6 ^ bit7
            if counter1024 == 128:
                counting1024odd = True
                counter1024=0


    Ecc0 = [P1024, P512, P256, P128, P64, P32, P16, P8, P4, P2, P1]
    # NOTE: padded with 1s to fill 24 bits
    Ecc1 = [1,1,P1024_1, P512_1, P256_1, P128_1, P64_1, P32_1, P16_1, P8_1, P4_1, P2_1, P1_1]
    return bytearray(list(reversed(list(getbytes(itertools.chain.from_iterable([Ecc1, Ecc0])))))[1:4])

if __name__ == '__main__':
    data1 = bytes.fromhex("""06 50 5F AD 00 00 A0 FF 00 00 00 00 F0 0B 00 00
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
""")

    data2 = bytes.fromhex("""4B E1 C0 FF 04 CC 24 48 1D 93 00 00 0F 60 2C E1
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
""")
    h = binascii.hexlify(crc(data1))
    print('data1 len:' + str(len(data1)))
    print('Flash block ECC:')
    print('Result (hex):\t%s' % h)
    assert(h == b'd64dd1')

    h2 = binascii.hexlify(crc(data2))
    print('data2 len:' + str(len(data2)))
    print('Flash block ECC:')
    print('Result (hex):\t%s' % h2)
    assert(h2 == b'78c7fb')

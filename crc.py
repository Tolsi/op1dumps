#!/usr/bin/env python3

def input_num_between_zero_and_n(max):
    r = -1
    while True:
        try:
            r = int(input())
            if r < 0 or r > max:
                print(f'Input number between 0 and {max}')
            else:
                return r
        except:
            print(f'Input number between 0 and {r}')

if __name__ == '__main__':
    base_address = int(format(1, '032b'), 2)
    segment_limit = int(format(1, '020b'), 2)
    g = 1
    l = 1
    db = 1
    avl = 1
    p = 1
    dpl = int(format(1, '2b'), 2)
    s = 1
    type = 1

    header = []
    header.append(format(base_address & 0xFF, '08b'))
    header.append(format(g, '01b'))
    header.append(hex(db)[2:])
    header.append(hex(l)[2:])
    header.append(bin(avl)[2:])
    header.append(format(segment_limit & 0xF, '04b'))
    header.append(bin(p)[2:])
    header.append(format(dpl, '02b'))
    header.append(bin(s)[2:])
    header.append(format(type, '04b'))
    header.append(format(base_address >> 8 & 0xFF, '08b'))
    header.append(format(base_address & 0xFFFF, '016b'))
    header.append(format(segment_limit >> 5, '016b'))
    b = ''.join(header)
    print('Memory descriptor:')
    print('bin:\t' + b)
    print('hex:\t' + hex(int(b, 2)))
    print('dec:\t' + str(int(b, 2)))

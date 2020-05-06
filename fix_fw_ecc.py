import array
import binascii
from pathlib import Path

import ADSP_ecc

def is_ff(data):
    for b in data:
        if b != 0xff:
            return False
    return True

if __name__ == '__main__':
    file = '/Users/tolsi/Documents/op-1-rev/MT29F4G08ABBDA@BGA63_2131_without_3627_BB.BIN'
    filebytes = array.array('B')
    filebytes.fromfile(open(file, 'rb'), Path(file).stat().st_size)

    data_size = 256 * 8
    ecc_size = 8 * 8
    page_size = data_size + ecc_size
    block_size = page_size * 64

    for block in range(0, 4096):
        for page in range(0, 64):
            start_index = block * block_size + page_size * page
            # data = filebytes[start_index:start_index + data_size]
            # ecc = filebytes[start_index + data_size:start_index + page_size]
            for i in range(0, 8):
                i_ecc = filebytes[start_index + data_size + i * 8:start_index + data_size + i * 8 + 3]
                i_data = filebytes[start_index + i * 256: start_index + i * 256 + 256]
                if not (is_ff(i_data) and is_ff(i_ecc)):
                    calc_ecc = ADSP_ecc.crc(i_data)
                    if i_ecc != calc_ecc:
                        print('Wrong ECC detected! Fixing: block %d, page %d, piece %d: %s -> %s' % (block, page, i, binascii.hexlify(i_ecc), binascii.hexlify(calc_ecc)))
                        filebytes[start_index + data_size + i * 8] = calc_ecc[0]
                        filebytes[start_index + data_size + i * 8+1] = calc_ecc[1]
                        filebytes[start_index + data_size + i * 8+2] = calc_ecc[2]
    print('Done!')

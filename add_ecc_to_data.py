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
    file = '/Users/tolsi/Documents/Music/OP-1/op-1-rev/old dump/PATCHED_MT29F4G08ABBDA@BGA63_2131_without_3627_BB_and_ECC.BIN'
    out_file = '/Users/tolsi/Documents/Music/OP-1/op-1-rev/old dump/PATCHED_MT29F4G08ABBDA@BGA63_2131_without_3627_BB.BIN'

    outbytes = array.array('B')
    filebytes = array.array('B')
    file_size = Path(file).stat().st_size
    filebytes.fromfile(open(file, 'rb'), file_size)

    blocks = 4096
    pages_in_block = 64
    data_in_page = 8

    page_bytes = array.array('B')
    ecc_bytes = array.array('B')

    def flush_to_bytes():
        outbytes.extend(page_bytes.tobytes())
        outbytes.extend(ecc_bytes.tobytes())
        del page_bytes[:]
        del ecc_bytes[:]

    for i in range(0, int(file_size / 256)):
            i_data = filebytes[i * 256: i * 256 + 256]

            if i % 8 == 0 and i > 0:
                flush_to_bytes()

            page_bytes.extend(i_data)
            if is_ff(i_data):
                ecc_bytes.extend([0xff] * 8)
            else:
                calc_ecc = ADSP_ecc.ecc(i_data)
                ecc_bytes.extend(calc_ecc)
                ecc_bytes.extend([0xff] * 5)

    flush_to_bytes()

    with open(out_file, "wb") as f:
        f.write(outbytes.tobytes())
    print('Done!')

import array
from pathlib import Path

find_first_bytes = 20

file = '/Users/tolsi/Documents/op-1-rev/MT29F4G08ABBDA@BGA63_2131_without_3627_BB.BIN'
filebytes = array.array('B')
filebytes.fromfile(open(file, 'rb'), Path(file).stat().st_size)
b = filebytes.tobytes()

for elem in Path('/Users/tolsi/Documents/op-1-rev/myfw/op1_241-repacked').rglob('*.*'):
    if not '/.' in str(elem):
        findBytes = array.array('B')
        read_bytes = min(find_first_bytes, elem.stat().st_size)
        findBytes.fromfile(open(str(elem), 'rb'), read_bytes)
        index = b.find(findBytes.tobytes())
        print('%s: offset %s (%d)' % (elem, hex(index) ,index))


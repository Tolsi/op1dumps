#!/usr/bin/env python3
"""
NOTE: this script is specific to MY OP-1 unit only. On a normal, healthy
OP-1, OTP page 0xD0 holds the correct XTEA key and none of this is needed.
On my unit, OTP page 0xD0 was accidentally overwritten with wrong data
(OTP is write-once, so it cannot be fixed in place) -- see the other
scripts/dumps in this repo for how that key page is normally used. As a
workaround I wrote the correct key bytes to the spare OTP page 0xE0
instead, and patched te-boot.ldr to read 0xE0 in place of 0xD0. This
script is the second half of that same D0->E0 workaround, needed only
for firmware v246 (see the two-part explanation below). Do not use this
on a device whose OTP page 0xD0 is intact.

OP-1 firmware v246 boot fix, for units with corrupted OTP page 0xD0
(the XTEA key page used by the bootloader) where a working key has
been written to the spare OTP page 0xE0 instead.

Two independent fixes, both required:

1. te-boot.ldr contains exactly one OTP read of page 0xD0 (used to set
   up the XTEA key for decrypting encrypted LDR blocks). Patched to
   read 0xE0 instead. Byte pattern, at file offset 0x150:
     1A 60 20 E1 D0 00 0D 9B 69 91 8D E6 01 00 69 91
                  ^^ D0 -> E0
   This alone is enough for firmware 243/245 (which contain no
   encrypted blocks) to boot.

2. Firmware 246's OP1_vdk.ldr adds ~46 new XTEA-encrypted LDR
   "callback" blocks (flags & 0x2400 == 0x2400), wrapping pre-existing
   boot-time init code (CRT/vector setup at target 0xffa00000, plus
   smaller helper blocks at 0xff8xxxxx/0xff9xxxxx) for anti-tamper
   purposes. Decryption key = 16 raw bytes of OTP page 0xD0 (same page
   as above, so whatever is at the unit's OTP 0xE0 after the fixup).

   The reference community decryptor (github.com/sualk/op1-decryptor,
   decrypt.c) has an edge-case bug: when a block's byte_count is not a
   multiple of 24, it leaves the final partial chunk completely
   untouched instead of decrypting it. 40 of the 46 blocks in 246 hit
   this case. The REAL hardware/encoder does not skip that tail: it
   forms the final 8-byte XTEA unit by reading past byte_count into
   the start of the *next* block's 16-byte header (always safe -- the
   header bytes immediately follow in the file). This script
   replicates that correctly; `decrypt_buf_naive` is kept only to show
   the bug for reference.

Usage:
    python3 patch_op1_246.py <otp_d0_hex32> <in_dir> <out_dir>

    otp_d0_hex32: 32 hex chars (16 bytes) = the known-good OTP page 0xD0
                  value (same bytes written to this unit's OTP 0xE0).
    in_dir:       unpacked firmware folder (te-boot.ldr, OP1_vdk.ldr, content/)
    out_dir:      where the patched folder is written; feed this to
                  `op1repacker repack <out_dir>`

Then flash the resulting .op1 via COM+Power as usual.
"""
import struct, sys, os, shutil

TE_BOOT_PATTERN_OLD = bytes.fromhex("1a6020e1d0000d9b69918de60100 6991".replace(" ", ""))
TE_BOOT_PATTERN_NEW = bytes.fromhex("1a6020e1e0000d9b69918de60100 6991".replace(" ", ""))


def decipher(num_cycles, v0, v1, k):
    delta = 0x9E3779B9
    mask = 0xFFFFFFFF
    s = (delta * num_cycles) & mask
    for _ in range(num_cycles):
        v1 = (v1 - ((((v0 << 4) & mask ^ (v0 >> 5)) + v0) ^ (s + k[(s >> 11) & 3]))) & mask
        s = (s - delta) & mask
        v0 = (v0 - ((((v1 << 4) & mask ^ (v1 >> 5)) + v1) ^ (s + k[s & 3]))) & mask
    return v0, v1


def decrypt_buf_correct(raw, content_off, bc, key):
    """Correct XTEA decrypt of one LDR block's content, matching real hardware:
    every 24-byte chunk has its first 8 bytes XTEA-deciphered; for the final
    partial chunk, the needed 8 bytes are read straight from the raw file
    (extending past byte_count into the next header if necessary)."""
    buf = bytearray(raw[content_off:content_off + bc])
    i = 0
    while i < bc:
        chunk_src = raw[content_off + i: content_off + i + 8]
        v0 = struct.unpack_from("<I", chunk_src, 0)[0]
        v1 = struct.unpack_from("<I", chunk_src, 4)[0]
        d0, d1 = decipher(32, v0, v1, key)
        dec8 = struct.pack("<II", d0, d1)
        take = min(8, bc - i)
        buf[i:i + take] = dec8[:take]
        i += 24
    return bytes(buf)


def walk_ldr_blocks(data):
    """Yield (header_off, flags, target, byte_count, argument, is_callback)
    for every block in an Analog Devices Blackfin LDR file."""
    off = 0
    n = len(data)
    blocks = []
    while off + 16 <= n:
        hdr = data[off:off + 16]
        if hdr[3] != 0xAD:
            break
        chk = 0
        for b in hdr:
            chk ^= b
        if chk != 0:
            break
        flags = struct.unpack_from("<H", hdr, 0)[0]
        target = struct.unpack_from("<I", hdr, 4)[0]
        byte_count = struct.unpack_from("<I", hdr, 8)[0]
        argument = struct.unpack_from("<I", hdr, 12)[0]
        is_cb = (flags & 0x2400) == 0x2400
        blocks.append((off, flags, target, byte_count, argument, is_cb))
        off += 16
        if flags & 0x100:
            continue
        if byte_count == 0:
            continue
        off += byte_count
    return blocks


def patch_te_boot(path_in, path_out):
    data = bytearray(open(path_in, "rb").read())
    idx = bytes(data).find(TE_BOOT_PATTERN_OLD)
    if idx < 0:
        if TE_BOOT_PATTERN_NEW in bytes(data):
            print("  te-boot.ldr: already patched, copying as-is")
            shutil.copy(path_in, path_out)
            return
        raise SystemExit("te-boot.ldr: expected OTP D0 read pattern not found -- different te-boot version?")
    data[idx:idx + len(TE_BOOT_PATTERN_NEW)] = TE_BOOT_PATTERN_NEW
    open(path_out, "wb").write(data)
    print(f"  te-boot.ldr: patched OTP page 0xD0 -> 0xE0 read at file offset {idx:#x}")


def patch_vdk(path_in, path_out, key):
    raw = open(path_in, "rb").read()
    blocks = walk_ldr_blocks(raw)
    out = bytearray(raw)
    n_patched = 0
    n_tail_fixed = 0
    for off, flags, target, bc, arg, is_cb in blocks:
        if not is_cb:
            continue
        new_flags = flags & ~0x2400
        struct.pack_into("<H", out, off, new_flags)
        out[off + 2] ^= 0x24  # checksum compensates for the flag change
        if bc > 0:
            dec = decrypt_buf_correct(raw, off + 16, bc, key)
            out[off + 16:off + 16 + bc] = dec
            if bc % 24 != 0:
                n_tail_fixed += 1
        n_patched += 1
    open(path_out, "wb").write(out)
    print(f"  OP1_vdk.ldr: decrypted and un-flagged {n_patched} callback blocks "
          f"({n_tail_fixed} needed the corrected tail-chunk handling)")


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        raise SystemExit(1)
    key_hex, in_dir, out_dir = sys.argv[1:4]
    if len(key_hex) != 32:
        raise SystemExit(f"OTP key must be exactly 32 hex chars (16 bytes), got {len(key_hex)}")
    key = struct.unpack(">IIII", bytes.fromhex(key_hex))

    os.makedirs(out_dir, exist_ok=True)
    print(f"Patching {in_dir} -> {out_dir}")
    patch_te_boot(os.path.join(in_dir, "te-boot.ldr"), os.path.join(out_dir, "te-boot.ldr"))
    patch_vdk(os.path.join(in_dir, "OP1_vdk.ldr"), os.path.join(out_dir, "OP1_vdk.ldr"), key)
    content_src = os.path.join(in_dir, "content")
    content_dst = os.path.join(out_dir, "content")
    if os.path.isdir(content_src) and not os.path.isdir(content_dst):
        shutil.copytree(content_src, content_dst)
        print("  content/: copied as-is")
    print(f"Done. Now run: op1repacker repack {out_dir!r}")


if __name__ == "__main__":
    main()

# op1 dumps

Small useful utilities to work with flash and CPU OTP dumps obtained for TE OP-1 repair.

# Scripts

* ADSP_ecc.py - script with implementation of ECC calculation for flash which is implemented in OP-1

* write_data_without_ecc.py - extract data from dump without ECC

* add_ecc_to_data.py  - insert ECC in data from dump (after changes of data from the previous script)

* check_fw.py - checks ECC in dump

* fix_fw_ecc.py - fix ECC in dump after changes

* find_files_offset_in_dump.py - looking for the entry of files from the firmware into the dump

* MT29F4G08 OP-1 Flash.bt - 010 Editor template file for the flash dump

* TE-OP1-board-useful-pins.jpg - Photo of the bottom of the board with the signed associated CPU legs

# Dumps

* TE-OP-1-BF524-OTP-dump.txt - OTP little-endian dump should to be written to the empty Blackfin BF524 processor to restore device boot.

* [TE-OP-1-flash-dump-fw241-boot-ok-formated-fw-MT29F4G08ABBDA@BGA63_2131.BIN.zip](https://github.com/Tolsi/op1dumps/raw/master/TE-OP-1-flash-dump-fw241-boot-ok-formated-fw-MT29F4G08ABBDA%40BGA63_2131.BIN.zip) - flash bump with worked boot v2.27 and empty formatted firmware v2.41

# OTP write details

Here's patched te-boot file to read and write a page to OP-1 OTP memory: `te-boot-otp-ops-2.28-10.ldr`. Use [op1repacker](https://github.com/op1hacks/op1repacker) to create a op1 firmware package to write from te-boot. Then enter to te-boot (press COM button during boot) and press 7 to read OTP memory (it's very fast, use a slow-motion camera to read it) or connect 7V to VPPOTP and press 2 to write it. Press button 2 several times until the menu is redrawn (it won't get any worse). 
You must write page by page (about 12 pages total) by making changes to this file at the following addresses:

`0x2d4d0-0x2d4df` - contains OTP data to write (little-endian)

`0xa642` - contains OTP page to write

Note that the system uses little endian, so you need to rearrange the bytes accordingly.

For example, here's a page readed from OTP:

`0xdf  20 45 47 41 4e 45 45 54	52 45 45 4e 49 47 4e 45`

Here it is in device memory (IDA LDR addressing):

```
DATA1:FF8059D0                 db 0x54 # T
DATA1:FF8059D1                 db 0x45 # E
DATA1:FF8059D2                 db 0x45 # E
DATA1:FF8059D3                 db 0x4E # N
DATA1:FF8059D4                 db 0x41 # A
DATA1:FF8059D5                 db 0x47 # G
DATA1:FF8059D6                 db 0x45 # E
DATA1:FF8059D7                 db 0x20

DATA1:FF8059D8                 db 0x45 # E
DATA1:FF8059D9                 db 0x4E # N
DATA1:FF8059DA                 db 0x47 # G
DATA1:FF8059DB                 db 0x49 # I
DATA1:FF8059DC                 db 0x4E # N
DATA1:FF8059DD                 db 0x45 # E
DATA1:FF8059DE                 db 0x45 # E
DATA1:FF8059DF                 db 0x52 # R
```

Note that this requires 6.9-7V to be applied to the VPPOTP CPU pin for a short time (it is brought to the board, check the board image), the chip cannot withstand such a voltage for more than 15 minutes in total. Disconnect the power pin before unplugging the power of the board or continuing to work with the boot menu to avoid interference and damage to the board.

Be sure to read the documentation for your processor before doing this. A data recorded once cannot be changed in OTP area!

Note that for te-boot to be successfully updated with firmware, it must have a different version from the current one (+/- 0.01 will be enough). Changing this is easy with a HEX editor - just change 4 occurrences of the current version in te-boot. Don't try this with <2 version of te-boot, you will get a brick! Only the flash programmer will restore your device after that.

For correct boot these pages must be written in OTP in the recommended order: 0x10-0x12, 0xd0-0xd3, 0xdf, 0xd8.

They are marked with an exclamation mark in the dump.

After writing 0xd8, the device will boot into the firmware (and this requires all previous entries), to enter te-boot again, you will need to hold down the COM button. Presumably 0x10-0x12 contains the code for start the firmware, and 0xd0-0xd3 for booting the device to the firmware. 0xdf is checked to validate the OTP record. The rest of the OTP pages data is the factory data about the processor.

If you want my OP-1 IDA Pro projects for your research - just ask.

# Acknowledgments

* Nanak0n aka Viktor89 for countless chip re-soldering on the knee and board analysis

* [tabascoeye](https://github.com/tabascoeye) for help and previous experiments with the device and Blackfin tool building, reading OTP dump

* Igor and Sergey - guys with the programmer for BGA63

# References

* [ADSP-BF52x Blackfin Processor Hardware Reference](https://www.analog.com/media/en/dsp-documentation/processor-manuals/ADSP-BF52x_hwr_rev1.2.pdf)

Contains a lot of data about CPU hardware: OTP and other.

* [Blackfin® Processor Programming Reference (includes ADSP-BF5xx and ADSP-BF60x Processors)](https://www.analog.com/media/en/dsp-documentation/processor-manuals/Blackfin_pgr_rev2.2.pdf) and [The Blackfin DSP Instruction Set Reference](http://smd.hu/Data/Analog/DSP/Blackfin/Blackfin_ISR_Nov14.pdf)

Contains Blackfin ASM details.

* [OP-1 Flash datasheet - Micron 2, 4, 8Gb: x8/x16 Multiplexed NAND Flash Memory Features](https://www.micron.com/-/media/client/global/documents/products/data-sheet/nand-flash/20-series/2gb_nand_m29b.pdf)

* [Micron TN-29-08: Hamming Codes for NAND Flash Memory Devices Overview](https://www.micron.com/-/media/client/global/documents/products/technical-note/nand-flash/tn2908_nand_hamming_ecc_code.pdf)

* [Micron TN-29-63: Error Correction Code (ECC) in SLC NAND Introduction](https://www.micron.com/-/media/client/global/documents/products/technical-note/nand-flash/tn2963_ecc_in_slc_nand.pdf)

* [OP-1 RAM datasheet - ISSI 42-45SM-RM-VM16320E](http://www.issi.com/WW/pdf/42-45SM-RM-VM16320E.pdf)

* [op1repacker](https://github.com/op1hacks/op1repacker)

* [Blackfin IDA Pro Plugin](https://github.com/op1hacks/Blackfin-IDA-Pro-Plugin)

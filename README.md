# op1flash

Small utilities and dumps obtained by TE OP-1 repair

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

Note that this requires 6.9-7V to be applied to the VPPOTP CPU pin for a short time (it is brought to the board, check the board image). Disconnect the power pin before unplugging the power of the board or continuing to work with the boot menu to avoid interference and damage to the board.

Be sure to read the documentation for your processor before doing this. A data recorded once cannot be changed!

* TE-OP-1-flash-dump-fw241-boot-ok-formated-fw-MT29F4G08ABBDA@BGA63_2131.BIN.zip - flash bump with worked boot v 2.27 and empty formatted firmware v2.41

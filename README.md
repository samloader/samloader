# samloader
Download firmware for Samsung devices (without any extra Windows drivers).
## Installation
```
pip3 install git+https://github.com/nlscc/samloader.git
```
## Usage
See `samloader --help` and `samloader (command) --help`.

`checkupdate`: Check the latest firmware version

`download`: Download the specified firmware version for a given phone and region to a specified file or directory

`decrypt`: Decrypt encrypted firmware
### Example
```
$ samloader -m GT-I8190N -r BTU checkupdate
I8190NXXAMJ2/I8190NBTUAMJ1/I8190NXXAMJ2/I8190NXXAMJ2
$ samloader -m GT-I8190N -r BTU download -v I8190NXXAMJ2/I8190NBTUAMJ1/I8190NXXAMJ2/I8190NXXAMJ2 -O .
downloading GT-I8190N_BTU_1_20131118100230_9ae3yzkqmu_fac.zip.enc2
[################################] 10570/10570 - 00:02:02
$ samloader -m GT-I8190N -r BTU decrypt -v I8190NXXAMJ2/I8190NBTUAMJ1/I8190NXXAMJ2/I8190NXXAMJ2 -V 2 -i GT-I8190N_BTU_1_20131118100230_9ae3yzkqmu_fac.zip.enc2 -o GT-I8190N_BTU_1_20131118100230_9ae3yzkqmu_fac.zip
[################################] 169115/169115 - 00:00:08
```

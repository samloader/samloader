# samloader
Download firmware for Samsung devices (without any extra Windows drivers).

## Project is archived
This project is no longer maintained. Please see [STATEMENT.pdf](STATEMENT.pdf).

### Licensing statement, June 19 2023

I, nlscc, the former maintainer of samloader, make the following statement:
```
LICENSE ADDENDUM STATEMENT

"Relevant Works" are the text of all commits authored by nlscc and uploaded
using the former nlscc GitHub account, insofar as they form a set of
instructions to modify a previous version of the source code (i.e. a set of
diffs), but excluding any text not authored by me but required to implement the
instructions.

The Relevant Works have been released into the public domain. Any previous
licenses applying to the Relevant Works are therefore null.

All rights vested in the Relevant Works, copyright or otherwise (including but
not limited to 'moral' rights), have been irreversibly waived, and
notwithstanding the above nlscc hereby covenants not to attempt to assert the
same.

For the avoidance of doubt this statement does not apply to commits authored by
people who are not nlscc.
```

## Installation
```
pip3 install git+https://github.com/samloader/samloader.git
```
## Usage
Run with `samloader` or `python3 -m samloader`. See `samloader --help` and `samloader (command) --help` for help.

`-m <model> -r <region> checkupdate`: Check the latest firmware version

`-m <model> -r <region> download -v <version> (-O <output-dir> or -o <output-file>)`: Download the specified firmware version for a given phone and region to a specified file or directory

`-m <model> -r <region> decrypt -v <version> -V <enc-version> -i <input-file> -o <output-file>`: Decrypt encrypted firmware
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
## Note
This project was formerly hosted at `nlscc/samloader`, and has moved to `samloader/samloader`.

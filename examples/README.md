# Pof examples

In this directory you'll find 2 files, the source and then generator file. The source file `source.py` contains the Python source file to obfuscate, and the generator file `gen.py` contain the obfuscator code. All outputs are produce to the `out/` directory.

This is useful to test pof, get a feel for the Python API, and how to use it, but also with some outputs and test the result.

Note that you'll need to install pof first.

## Verify

You can verify that the obfuscated outputs are valid by just running them:

```bash
$ python3 basic.py
My pet is name: aabocaye

$ python3 custom_complete.py
My pet is name: ufvlwqot

# NOTE: this one may fail if you trigger the evasion, so this is normal
$ python3 evasion_basic.py
My pet is name: vpdqkofy
```

Or you can verify by running every output files:

```bash
$ ./run_all.sh
My pet is name: asesufdl
My pet is name: zntqagwv
My pet is name: fpeygrtt
My pet is name: trhkchrb
My pet is name: svbzhrlj
My pet is name: orxxqsnk
My pet is name: sepwpfqh
My pet is name: qvstoywr
My pet is name: jpxhsuwp
My pet is name: hdjkuzyg
My pet is name: mjjndrqb
My pet is name: aixmaamv
My pet is name: ixkugvpc
My pet is name: jvkhdgbd
My pet is name: qqbpcnia
My pet is name: fjerllhp
My pet is name: vcyvsqbu
```

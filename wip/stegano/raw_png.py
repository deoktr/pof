"""PNG format:

```
.PNG........IHDR
..............wS
.....IDAT..c....
.............IEN
D.B`.
```

raw:
```
89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52
00 00 00 01 00 00 00 01 08 02 00 00 00 90 77 53
DE 00 00 00 0C 49 44 41 54 08 D7 63 F8 CF C0 00
00 03 01 01 00 18 DD 8D B0 00 00 00 00 49 45 4E
44 AE 42 60 82
```
"""


def raw_png_data(content):
    # content start at 0x49484452
    return content


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "rb") as f:
        content = f.read()

    print(raw_png_data(content))

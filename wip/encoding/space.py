# add and get the spaces and tab from the end of the source file lines
import re


def sntencode(msg):
    """Space and tab (snp) encode."""
    msg_bin = bin(int.from_bytes(msg, "big")).replace("0b", "")
    out = ""
    for bit in msg_bin:
        if bit == "0":
            out += " "
        elif bit == "1":
            out += "\t"
    return out


def sntdecode(encoded):
    """Space and tab (snp) decode."""
    msg_bin = encoded.replace(" ", "0").replace("\t", "1")
    n = int(msg_bin, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, "big")


def sntencode_trailing(source, msg):
    snt = sntencode(msg)
    lines = source.count("\n")
    chunk_size = int(len(snt) / lines)
    snt_chunks = [snt[i : i + chunk_size] for i in range(0, len(snt), chunk_size)]

    out = ""
    for index, line in enumerate(source.split("\n")):
        chunk = ""
        if len(snt_chunks) > index:
            chunk = snt_chunks[index]
        out += line + chunk + "\n"

    return out


def sntdecode_trailing(source):
    r = "[ \t]+$"
    m = re.findall(r, source.decode(), re.MULTILINE)
    snt = "".join(m)
    return sntdecode(snt)


if __name__ == "__main__":
    msg = b"Hello"

    source = """
for x in range(0, 12):
    print(x)

# test comment
if False:
    print('ha')
"""

    esource = sntencode_trailing(source, msg)
    print(repr(esource))

    print(sntdecode_trailing(esource.encode()))

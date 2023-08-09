import io
from tokenize import generate_tokens, untokenize

from pof.obfuscator import PrintObfuscator

source = """
import foo
from bar import koo
a=1
print("Hello, world!")
print(a)
a+=1
print(f"{a}")
print("aa", "oo")
print(foo())
print(foo("ho", koo(), "j", 42), "e")
if __name__ == "__main__":
    koo(a)
"""

result = '\nimport foo \nfrom bar import koo \na =1 \n\n\na +=1 \n\n\n\n\nif __name__ =="__main__":\n    koo (a )\n'


def test_PrintObfuscator():
    io_obj = io.StringIO(source)
    tokens = list(generate_tokens(io_obj.readline))
    tokens = PrintObfuscator().obfuscate_tokens(tokens)

    for _index, (_toknum, tokval, *_) in enumerate(tokens):
        assert tokval != "print"

    out = untokenize(tokens)
    assert out == result

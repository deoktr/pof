import io
from tokenize import generate_tokens, untokenize

from pof.obfuscator import Base32HexObfuscator

source = """
def main_function():
    x = "Hello"
    y = ", world!"
    print(x + y)

main_function()
"""


def test_Base32HexObfuscator():
    io_obj = io.StringIO(source)
    tokens = list(generate_tokens(io_obj.readline))
    tokens = Base32HexObfuscator().obfuscate_tokens(tokens)

    out = untokenize(tokens)
    exec(out)

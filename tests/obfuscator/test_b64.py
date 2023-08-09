import io
from tokenize import generate_tokens, untokenize

from pof.obfuscator import Base64Obfuscator

source = """
def main_function():
    x = "Hello"
    y = ", world!"
    print(x + y)

main_function()
"""


def test_Base64Obfuscator():
    io_obj = io.StringIO(source)
    tokens = list(generate_tokens(io_obj.readline))
    tokens = Base64Obfuscator().obfuscate_tokens(tokens)

    out = untokenize(tokens)
    exec(out)

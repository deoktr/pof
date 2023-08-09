import io
from base64 import b64decode  # noqa

# to fix a problem "undefined b64decode" during exec
from tokenize import generate_tokens, untokenize

from pof.obfuscator import XORObfuscator

source = """
def main_function():
    x = "Hello"
    y = ", world!"
    print(x + y)

main_function()
"""


def test_XORObfuscator():
    io_obj = io.StringIO(source)
    tokens = list(generate_tokens(io_obj.readline))
    tokens = XORObfuscator().obfuscate_tokens(tokens)

    out = untokenize(tokens)
    exec(out)

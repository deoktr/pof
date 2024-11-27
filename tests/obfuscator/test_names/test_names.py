import io
import os
from tokenize import generate_tokens, untokenize

from pof.obfuscator import NamesObfuscator


# FIXME (deoktr): mock the generator function inside NamesObfuscator
# to produce var_name__, because if we put generator "O" then it will break with
def test_NamesObfuscator():
    def generator():
        while True:
            yield "O"

    source_file_path = os.path.join(os.path.dirname(__file__), "code", "source.py")
    with open(source_file_path) as f:
        source = f.read()

    io_obj = io.StringIO(source)
    tokens = list(generate_tokens(io_obj.readline))

    tokens = NamesObfuscator(generator=generator()).obfuscate_tokens(tokens)

    out = untokenize(tokens) + "\n"

    out_file_path = os.path.join(os.path.dirname(__file__), "code", "out.py")
    with open(out_file_path) as f:
        out_wanted = f.read()

    assert out == out_wanted

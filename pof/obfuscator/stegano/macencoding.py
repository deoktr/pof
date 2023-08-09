from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.stegano import MACEncoding
from pof.utils.tokens import untokenize


class MACObfuscator(MACEncoding):
    """Encode the source code in a list of valid MAC."""

    def obfuscate_tokens(cls, tokens):
        code = untokenize(tokens)
        return [
            *cls.import_tokens(),
            (NEWLINE, "\n"),
            (NAME, "exec"),
            (LPAR, "("),
            *cls.decode_tokens(cls.encode_tokens(code.encode())),
            (RPAR, ")"),
            (NEWLINE, "\n"),
        ]

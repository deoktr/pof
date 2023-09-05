from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.encoding import BinasciiEncoding
from pof.utils.tokens import untokenize


class BinasciiObfuscator(BinasciiEncoding):
    """Obfuscate with encoding format Binascii."""

    @classmethod
    def obfuscate_tokens(cls, tokens):
        """Generate payload to execute the binascii encoded code."""
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

from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.compression import ZlibCompression
from pof.utils.tokens import untokenize


class ZlibObfuscator(ZlibCompression):
    """ZLIB compression obfuscator."""

    @classmethod
    def obfuscate_tokens(cls, tokens):
        """Generate payload to execute the zlib encoded code."""
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

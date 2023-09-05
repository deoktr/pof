from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.compression import LzmaCompression
from pof.utils.tokens import untokenize


class LzmaObfuscator(LzmaCompression):
    """LZMA compression obfuscator."""

    @classmethod
    def obfuscate_tokens(cls, tokens):
        """Generate payload to execute the lzma encoded code."""
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

from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.compression import GzipCompression
from pof.utils.tokens import untokenize


class GzipObfuscator(GzipCompression):
    @classmethod
    def obfuscate_tokens(cls, tokens):
        """Generate payload to execute the gzip encoded code."""
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

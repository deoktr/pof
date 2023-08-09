from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.compression import Bz2Compression
from pof.utils.tokens import untokenize


class Bz2Obfuscator(Bz2Compression):
    @classmethod
    def obfuscate_tokens(cls, tokens):
        """Generate payload to execute the bz2 encoded code."""
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

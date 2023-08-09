from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.stegano import IPv6Encoding
from pof.utils.tokens import untokenize


class IPv6Obfuscator(IPv6Encoding):
    """Encode the source code in a list of valid IPv6."""

    @classmethod
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

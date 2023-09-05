from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.encoding import Base32HexEncoding
from pof.utils.tokens import untokenize


class Base32HexObfuscator(Base32HexEncoding):
    """Obfuscate with encoding format Base32Hex."""

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

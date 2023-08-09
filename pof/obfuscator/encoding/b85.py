from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.encoding import Base85Encoding
from pof.utils.tokens import untokenize


class Base85Obfuscator(Base85Encoding):
    """Base85 encoding.

    New in Python version 3.4
    """

    @classmethod
    def obfuscate_tokens(cls, tokens):
        """Generate payload to execute the base85 encoded code."""
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

from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.encoding import SpacenTabEncoding
from pof.utils.tokens import untokenize


class SpacenTabObfuscator(SpacenTabEncoding):
    @classmethod
    def obfuscate_tokens(cls, tokens):
        code = untokenize(tokens)
        return [
            *cls.import_tokens(),
            (NEWLINE, "\n"),
            *cls.definition_tokens(),
            (NEWLINE, "\n"),
            (NAME, "exec"),
            (LPAR, "("),
            *cls.decode_tokens(cls.encode_tokens(code.encode())),
            (RPAR, ")"),
            (NEWLINE, "\n"),
        ]

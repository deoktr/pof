from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.cipher import ShiftCipher
from pof.utils.tokens import untokenize


class ShiftObfuscator(ShiftCipher):
    @classmethod
    def obfuscate_tokens(cls, tokens):
        code = untokenize(tokens)
        return [
            (NAME, "exec"),
            (LPAR, "("),
            *cls.decode_tokens(cls.encode_tokens(code)),
            (RPAR, ")"),
            (NEWLINE, "\n"),
        ]

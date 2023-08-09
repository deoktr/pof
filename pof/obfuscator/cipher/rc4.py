from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.cipher import RC4Cipher
from pof.utils.tokens import untokenize


class RC4Obfuscator(RC4Cipher):
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
            *cls.decode_tokens(cls.encode_tokens(code)),
            (RPAR, ")"),
            (NEWLINE, "\n"),
        ]

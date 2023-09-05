from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.cipher import RC4Cipher
from pof.utils.tokens import untokenize


class RC4Obfuscator(RC4Cipher):
    """RC4 cipher obfuscator."""

    def obfuscate_tokens(self, tokens):
        code = untokenize(tokens)
        return [
            *self.import_tokens(),
            (NEWLINE, "\n"),
            *self.definition_tokens(),
            (NEWLINE, "\n"),
            (NAME, "exec"),
            (LPAR, "("),
            *self.decode_tokens(self.encode_tokens(code)),
            (RPAR, ")"),
            (NEWLINE, "\n"),
        ]

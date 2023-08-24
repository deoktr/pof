from tokenize import LPAR, NAME, NEWLINE, NUMBER, OP, RPAR

from pof.utils.cipher import RC4Cipher
from pof.utils.tokens import untokenize


class RC4Stager(RC4Cipher):
    """Takes the key as first argument to decrypt and execute."""

    def generate_stager(self, tokens):
        code = untokenize(tokens)
        key_tokens = [
            (NAME, "sys"),
            (OP, "."),
            (NAME, "argv"),
            (OP, "."),
            (NAME, "pop"),
            (OP, "("),
            (NUMBER, "1"),
            (OP, ")"),
        ]

        return [
            (NAME, "import"),
            (NAME, "sys"),
            (NEWLINE, "\n"),
            *self.import_tokens(),
            (NEWLINE, "\n"),
            *self.definition_tokens(),
            (NEWLINE, "\n"),
            (NAME, "exec"),
            (LPAR, "("),
            *self.decode_tokens(self.encode_tokens(code), key_tokens=key_tokens),
            (RPAR, ")"),
            (NEWLINE, "\n"),
        ]

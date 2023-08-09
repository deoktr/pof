from tokenize import LPAR, NAME, NUMBER, OP, RPAR, STRING


class ShiftCipher:
    """Shift/Caesar cipher."""

    def __init__(self, padding=3) -> None:
        self.padding = padding

    @staticmethod
    def import_tokens():
        return []

    def encode_tokens(self, string):
        cipher = "".join([chr(ord(i) + self.padding) for i in string])
        return [(STRING, repr(cipher))]

    def decode_tokens(self, encoded_tokens):
        """`"".join([chr(ord(i)-3) for i in "Khoor/#Zruog$"])`."""
        return [
            (STRING, '""'),
            (OP, "."),
            (NAME, "join"),
            (LPAR, "("),
            (OP, "["),
            (NAME, "chr"),
            (LPAR, "("),
            (NAME, "ord"),
            (LPAR, "("),
            (NAME, "i"),
            (RPAR, ")"),
            (OP, "-"),
            (NUMBER, str(self.padding)),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "i"),
            (NAME, "in"),
            *encoded_tokens,
            (OP, "]"),
            (RPAR, ")"),
        ]

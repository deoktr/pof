from base64 import a85encode
from tokenize import LPAR, NAME, RPAR, STRING


class ASCII85Encoding:
    """ASCII85 encoding.

    New in Python version 3.4
    """

    @staticmethod
    def encode(string):
        return a85encode(string).decode()

    @classmethod
    def encode_tokens(cls, string):
        return [(STRING, repr(cls.encode(string)))]

    @staticmethod
    def import_tokens():
        return [
            (NAME, "from"),
            (NAME, "base64"),
            (NAME, "import"),
            (NAME, "a85decode"),
        ]

    @staticmethod
    def decode_tokens(encoded_tokens):
        return [
            (NAME, "a85decode"),
            (LPAR, "("),
            *encoded_tokens,
            (RPAR, ")"),
        ]

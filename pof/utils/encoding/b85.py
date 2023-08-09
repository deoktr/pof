from base64 import b85encode
from tokenize import LPAR, NAME, RPAR, STRING


class Base85Encoding:
    """Base85 encoding.

    New in Python version 3.4
    """

    @staticmethod
    def encode(string):
        return b85encode(string).decode()

    @classmethod
    def encode_tokens(cls, string):
        return [(STRING, repr(cls.encode(string)))]

    @staticmethod
    def import_tokens():
        return [
            (NAME, "from"),
            (NAME, "base64"),
            (NAME, "import"),
            (NAME, "b85decode"),
        ]

    @staticmethod
    def decode_tokens(encoded_tokens):
        return [
            (NAME, "b85decode"),
            (LPAR, "("),
            *encoded_tokens,
            (RPAR, ")"),
        ]

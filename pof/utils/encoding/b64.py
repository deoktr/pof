from base64 import b64encode
from tokenize import LPAR, NAME, RPAR, STRING


class Base64Encoding:
    @staticmethod
    def encode(string):
        return b64encode(string).decode()

    @classmethod
    def encode_tokens(cls, string):
        return [(STRING, repr(cls.encode(string)))]

    @staticmethod
    def import_tokens():
        return [
            (NAME, "from"),
            (NAME, "base64"),
            (NAME, "import"),
            (NAME, "b64decode"),
        ]

    @staticmethod
    def decode_tokens(encoded_tokens):
        return [
            (NAME, "b64decode"),
            (LPAR, "("),
            *encoded_tokens,
            (RPAR, ")"),
        ]

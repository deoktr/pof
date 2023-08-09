from base64 import b16encode
from tokenize import LPAR, NAME, RPAR, STRING


class Base16Encoding:
    @staticmethod
    def encode(string):
        return b16encode(string).decode()

    @classmethod
    def encode_tokens(cls, string):
        return [(STRING, repr(cls.encode(string)))]

    @staticmethod
    def import_tokens():
        return [
            (NAME, "from"),
            (NAME, "base64"),
            (NAME, "import"),
            (NAME, "b16decode"),
        ]

    @staticmethod
    def decode_tokens(encoded_tokens):
        return [
            (NAME, "b16decode"),
            (LPAR, "("),
            *encoded_tokens,
            (RPAR, ")"),
        ]

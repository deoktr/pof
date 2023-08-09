from base64 import b32encode
from tokenize import LPAR, NAME, RPAR, STRING


class Base32Encoding:
    @staticmethod
    def encode(string):
        return b32encode(string).decode()

    @classmethod
    def encode_tokens(cls, string):
        return [(STRING, repr(cls.encode(string)))]

    @staticmethod
    def import_tokens():
        return [
            (NAME, "from"),
            (NAME, "base64"),
            (NAME, "import"),
            (NAME, "b32decode"),
        ]

    @staticmethod
    def decode_tokens(encoded_tokens):
        return [
            (NAME, "b32decode"),
            (LPAR, "("),
            *encoded_tokens,
            (RPAR, ")"),
        ]

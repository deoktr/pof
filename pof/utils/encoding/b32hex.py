from base64 import b32hexencode
from tokenize import LPAR, NAME, RPAR, STRING


class Base32HexEncoding:
    @staticmethod
    def encode(string):
        return b32hexencode(string).decode()

    @classmethod
    def encode_tokens(cls, string):
        return [(STRING, repr(cls.encode(string)))]

    @staticmethod
    def import_tokens():
        return [
            (NAME, "from"),
            (NAME, "base64"),
            (NAME, "import"),
            (NAME, "b32hexdecode"),
        ]

    @staticmethod
    def decode_tokens(encoded_tokens):
        return [
            (NAME, "b32hexdecode"),
            (LPAR, "("),
            *encoded_tokens,
            (RPAR, ")"),
        ]

import binascii
import marshal
from tokenize import COMMA, LPAR, NAME, OP, RPAR, STRING


class BinasciiEncoding:
    @staticmethod
    def encode(string):
        return binascii.b2a_base64(marshal.dumps(string))

    @classmethod
    def encode_tokens(cls, string):
        return [(STRING, repr(cls.encode(string)))]

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "binascii"),
            (COMMA, ","),
            (NAME, "marshal"),
        ]

    @staticmethod
    def decode_tokens(encoded_tokens):
        return [
            (NAME, "marshal"),
            (OP, "."),
            (NAME, "loads"),
            (LPAR, "("),
            (NAME, "binascii"),
            (OP, "."),
            (NAME, "a2b_base64"),
            (LPAR, "("),
            *encoded_tokens,
            (RPAR, ")"),
            (RPAR, ")"),
        ]

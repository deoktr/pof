import bz2
import marshal
from tokenize import COMMA, LPAR, NAME, OP, RPAR, STRING


class Bz2Compression:
    @staticmethod
    def encode(string):
        return bz2.compress(marshal.dumps(string))

    @classmethod
    def encode_tokens(cls, string):
        return [(STRING, repr(cls.encode(string)))]

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "bz2"),
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
            (NAME, "bz2"),
            (OP, "."),
            (NAME, "decompress"),
            (LPAR, "("),
            *encoded_tokens,
            (RPAR, ")"),
            (RPAR, ")"),
        ]

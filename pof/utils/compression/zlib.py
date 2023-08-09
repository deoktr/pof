import marshal
import zlib
from tokenize import COMMA, LPAR, NAME, OP, RPAR, STRING


class ZlibCompression:
    @staticmethod
    def encode(string):
        return zlib.compress(marshal.dumps(string))

    @classmethod
    def encode_tokens(cls, string):
        return [(STRING, repr(cls.encode(string)))]

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "zlib"),
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
            (NAME, "zlib"),
            (OP, "."),
            (NAME, "decompress"),
            (LPAR, "("),
            *encoded_tokens,
            (RPAR, ")"),
            (RPAR, ")"),
        ]

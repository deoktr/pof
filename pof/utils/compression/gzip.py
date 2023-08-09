import gzip
import marshal
from tokenize import COMMA, LPAR, NAME, OP, RPAR, STRING


class GzipCompression:
    @staticmethod
    def encode(string):
        return gzip.compress(marshal.dumps(string))

    @classmethod
    def encode_tokens(cls, string):
        return [(STRING, repr(cls.encode(string)))]

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "gzip"),
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
            (NAME, "gzip"),
            (OP, "."),
            (NAME, "decompress"),
            (LPAR, "("),
            *encoded_tokens,
            (RPAR, ")"),
            (RPAR, ")"),
        ]

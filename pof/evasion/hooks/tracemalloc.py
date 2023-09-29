from tokenize import LPAR, NAME, OP, RPAR

from pof.evasion.base import BaseEvasion


class TracemallocEvasion(BaseEvasion):
    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "tracemalloc"),
        ]

    @staticmethod
    def check_tokens():
        """`tracemalloc.is_tracing()`."""
        return [
            (NAME, "tracemalloc"),
            (OP, "."),
            (NAME, "is_tracing"),
            (LPAR, "("),
            (RPAR, ")"),
        ]

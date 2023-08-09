from tokenize import LPAR, NAME, OP, RPAR

from pof.evasion.base import BaseEvasion


class TracemallocEvasion(BaseEvasion):
    def import_tokens(self):
        return [
            (NAME, "import"),
            (NAME, "tracemalloc"),
        ]

    def check_tokens(self):
        """`tracemalloc.is_tracing()`."""
        return [
            (NAME, "tracemalloc"),
            (OP, "."),
            (NAME, "is_tracing"),
            (LPAR, "("),
            (RPAR, ")"),
        ]

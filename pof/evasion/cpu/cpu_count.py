from tokenize import LPAR, NAME, NUMBER, OP, RPAR

from pof.evasion.base import BaseEvasion


class CPUCountEvasion(BaseEvasion):
    def __init__(self, min_cpu_count: int = 2) -> None:
        self.min_cpu_count = min_cpu_count

    def import_tokens(self) -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "multiprocessing"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """`multiprocessing.cpu_count() < 2`."""
        return [
            (NAME, "multiprocessing"),
            (OP, "."),
            (NAME, "cpu_count"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.min_cpu_count)),
        ]

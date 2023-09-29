# TODO (204): make windows version
from tokenize import LPAR, NAME, NUMBER, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class LinuxRAMCountEvasion(BaseEvasion):
    def __init__(self, min_ram: int = 2) -> None:
        """Min RAM in Gib."""
        self.min_ram = min_ram

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """Linux RAM count evasion tokens.

        `((os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')) / (1024.**3)) < 2`
        """
        return [
            (LPAR, "("),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "sysconf"),
            (LPAR, "("),
            (STRING, "'SC_PAGE_SIZE'"),
            (RPAR, ")"),
            (OP, "*"),
            (NAME, "os"),
            (OP, "."),
            (NAME, "sysconf"),
            (LPAR, "("),
            (STRING, "'SC_PHYS_PAGES'"),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "/"),
            (LPAR, "("),
            (NUMBER, "1024."),
            (OP, "**"),
            (NUMBER, "3"),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.min_ram)),
        ]

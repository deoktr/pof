# TODO (204): make a version for windows
from tokenize import LPAR, NAME, NUMBER, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class LinuxProcCountEvasion(BaseEvasion):
    def __init__(self, proc_count=100) -> None:
        self.proc_count = proc_count

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self):
        """`len(list(filter(lambda d: d.isdigit(), os.listdir("/proc")))) < 100`."""
        return [
            (NAME, "len"),
            (LPAR, "("),
            (NAME, "list"),
            (LPAR, "("),
            (NAME, "filter"),
            (LPAR, "("),
            (NAME, "lambda"),
            (NAME, "d"),
            (OP, ":"),
            (NAME, "d"),
            (OP, "."),
            (NAME, "isdigit"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, ","),
            (NAME, "os"),
            (OP, "."),
            (NAME, "listdir"),
            (LPAR, "("),
            (STRING, repr("/proc")),
            (RPAR, ")"),
            (RPAR, ")"),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.proc_count)),
        ]

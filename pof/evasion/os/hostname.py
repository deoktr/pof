from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class HostnameEvasion(BaseEvasion):
    def __init__(self, hostname) -> None:
        self.hostname = hostname

    def import_tokens(self):
        return [
            (NAME, "import"),
            (NAME, "socket"),
        ]

    def check_tokens(self):
        """`socket.gethostname()!='debian'`."""
        return [
            (NAME, "socket"),
            (OP, "."),
            (NAME, "gethostname"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "!="),
            (STRING, repr(self.hostname)),
        ]

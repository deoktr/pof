from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class DomainEvasion(BaseEvasion):
    def __init__(self, domain) -> None:
        self.domain = domain

    def import_tokens(self):
        return [
            (NAME, "import"),
            (NAME, "socket"),
        ]

    def check_tokens(self):
        """`socket.getfqdn()!='debian'`."""
        return [
            (NAME, "socket"),
            (OP, "."),
            (NAME, "getfqdn"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "!="),
            (STRING, repr(self.domain)),
        ]

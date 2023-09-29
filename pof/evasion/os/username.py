from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class UsernameEvasion(BaseEvasion):
    def __init__(self, username) -> None:
        self.username = username

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "getpass"),
        ]

    def check_tokens(self):
        """`getpass.getuser()!='username'`."""
        return [
            (NAME, "getpass"),
            (OP, "."),
            (NAME, "getuser"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "!="),
            (STRING, repr(self.username)),
        ]

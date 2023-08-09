from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class FileExistEvasion(BaseEvasion):
    def __init__(self, file) -> None:
        self.file = file

    def import_tokens(self):
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self):
        """`not os.path.isfile('/tmp/a')`."""
        return [
            (NAME, "not"),
            (NAME, "os"),
            (OP, "."),
            (NAME, "path"),
            (OP, "."),
            (NAME, "isfile"),
            (LPAR, "("),
            (STRING, repr(self.file)),
            (RPAR, ")"),
        ]

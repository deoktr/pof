from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class DirectoryExistEvasion(BaseEvasion):
    def __init__(self, directory) -> None:
        self.directory = directory

    def import_tokens(self):
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self):
        """`not os.path.isdir('/tmp/a')`."""
        return [
            (NAME, "not"),
            (NAME, "os"),
            (OP, "."),
            (NAME, "path"),
            (OP, "."),
            (NAME, "isdir"),
            (LPAR, "("),
            (STRING, repr(self.directory)),
            (RPAR, ")"),
        ]

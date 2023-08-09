from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class DirectoryMissingEvasion(BaseEvasion):
    def __init__(self, directory) -> None:
        self.directory = directory

    def import_tokens(self):
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self):
        """`os.path.isdir('/tmp/a')`."""
        return [
            (NAME, "os"),
            (OP, "."),
            (NAME, "path"),
            (OP, "."),
            (NAME, "isdir"),
            (LPAR, "("),
            (STRING, repr(self.directory)),
            (RPAR, ")"),
        ]

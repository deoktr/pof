from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class FileMissingEvasion(BaseEvasion):
    def __init__(self, file) -> None:
        self.file = file

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self):
        """Trigger evasion if a file is present on the system.

        `os.path.isfile('/tmp/a')`
        """
        return [
            (NAME, "os"),
            (OP, "."),
            (NAME, "path"),
            (OP, "."),
            (NAME, "isfile"),
            (LPAR, "("),
            (STRING, repr(self.file)),
            (RPAR, ")"),
        ]

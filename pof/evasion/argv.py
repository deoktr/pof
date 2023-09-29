from tokenize import NAME, NUMBER, OP, STRING

from pof.evasion.base import BaseEvasion


class ArgvEvasion(BaseEvasion):
    """Ensure that the correct argument is passed."""

    def __init__(self, argv="argv", position=1) -> None:
        self.argv = argv
        # can put -1 in position to select the last argument
        self.position = position

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "sys"),
        ]

    def check_tokens(self):
        """Validates system does not use UTC timezone.

        `len(sys.argv)==1 or sys.argv[1]!="123"`
        """
        return [
            (NAME, "len"),
            (OP, "("),
            (NAME, "sys"),
            (OP, "."),
            (NAME, "argv"),
            (OP, ")"),
            (OP, "=="),
            (NUMBER, str(self.position)),
            (NAME, "or"),
            (NAME, "sys"),
            (OP, "."),
            (NAME, "argv"),
            (OP, "["),
            (NUMBER, str(self.position)),
            (OP, "]"),
            (OP, "!="),
            (STRING, repr(self.argv)),
        ]

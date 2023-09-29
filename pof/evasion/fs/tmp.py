from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class TmpCountEvasion(BaseEvasion):
    """Cross-platform evasion that count the number of temp files."""

    def __init__(self, tmp_count=5) -> None:
        self.tmp_count = tmp_count

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
            (OP, ","),
            (NAME, "sys"),
        ]

    def check_tokens(self):
        r"""Check the number of files present in /tmp.

        `len(os.listdir("/tmp"if sys.platform!="windows"else"C:\windows\temp"))<10`
        """
        return [
            (NAME, "len"),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "listdir"),
            (LPAR, "("),
            (STRING, repr("/tmp")),  # noqa: S108
            (NAME, "if"),
            (NAME, "sys"),
            (OP, "."),
            (NAME, "platform"),
            (OP, "!="),
            (STRING, repr("windows")),
            (NAME, "else"),
            (STRING, repr("C:\\windows\\temp")),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "<"),
            (STRING, repr(self.tmp_count)),
        ]


class LinuxTmpCountEvasion(BaseEvasion):
    def __init__(self, tmp_count=5) -> None:
        self.tmp_count = tmp_count

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
            (OP, ","),
            (NAME, "sys"),
        ]

    def check_tokens(self):
        """Check the number of files present in /tmp.

        `len(os.listdir("/tmp")) < 10`
        """
        return [
            (NAME, "len"),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "listdir"),
            (LPAR, "("),
            (STRING, repr("/tmp")),  # noqa: S108
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "<"),
            (STRING, repr(self.tmp_count)),
        ]


class WinTmpCountEvasion(BaseEvasion):
    def __init__(self, tmp_count=5) -> None:
        self.tmp_count = tmp_count

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
            (OP, ","),
            (NAME, "sys"),
        ]

    def check_tokens(self):
        r"""Check the number of files present in /tmp.

        `len(os.listdir("C:\windows\temp")) < 10`
        """
        return [
            (NAME, "len"),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "listdir"),
            (LPAR, "("),
            (STRING, repr(r"C:\windows\temp")),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "<"),
            (STRING, repr(self.tmp_count)),
        ]

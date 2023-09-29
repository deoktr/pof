# TODO (204): make it compatible with windows: `ctypes.windll.shell32.IsUserAnAdmin()`
from tokenize import LPAR, NAME, NUMBER, OP, RPAR

from pof.evasion.base import BaseEvasion


class LinuxUIDEvasion(BaseEvasion):
    def __init__(self, uid) -> None:
        self.uid = uid

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self):
        """`os.getuid()!=1000`."""
        return [
            (NAME, "os"),
            (OP, "."),
            (NAME, "getuid"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "!="),
            (NUMBER, str(self.uid)),
        ]

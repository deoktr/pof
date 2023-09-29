from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class DebuggerEvasion(BaseEvasion):
    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "sys"),
        ]

    @staticmethod
    def check_tokens():
        """Detect Python debugger.

        `hasattr(sys, 'gettrace') and sys.gettrace() is not None`
        """
        return [
            (NAME, "hasattr"),
            (LPAR, "("),
            (NAME, "sys"),
            (OP, ","),
            (STRING, "'gettrace'"),
            (RPAR, ")"),
            (NAME, "and"),
            (NAME, "sys"),
            (OP, "."),
            (NAME, "gettrace"),
            (LPAR, "("),
            (RPAR, ")"),
            (NAME, "is"),
            (NAME, "not"),
            (NAME, "None"),
        ]

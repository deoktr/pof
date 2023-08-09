from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class DebuggerEvasion(BaseEvasion):
    def import_tokens(self):
        return [
            (NAME, "import"),
            (NAME, "sys"),
        ]

    def check_tokens(self):
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

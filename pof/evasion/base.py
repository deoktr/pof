from tokenize import DEDENT, INDENT, LPAR, NAME, NEWLINE, OP, RPAR, STRING


class BaseEvasion:
    # add evasion class name inside the exception
    ADD_CLASS_NAME = True

    @classmethod
    def fail_call_tokens(cls):
        return [
            (NAME, "raise"),
            (NAME, "Exception"),
            (LPAR, "("),
            (
                STRING,
                (
                    repr(cls.__class__.__name__)
                    if cls.ADD_CLASS_NAME
                    else repr("evasion check triggered")
                ),
            ),
            (RPAR, ")"),
        ]

    @staticmethod
    def import_tokens():
        return []

    @staticmethod
    def check_tokens():
        return []

    def add_evasion(self, tokens):
        return [
            *self.import_tokens(),
            (NEWLINE, "\n"),
            (NAME, "if"),
            (LPAR, "("),
            *self.check_tokens(),
            (RPAR, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "    "),
            *self.fail_call_tokens(),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            *tokens,
        ]

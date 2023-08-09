from tokenize import DEDENT, INDENT, LPAR, NAME, NEWLINE, OP, RPAR, STRING


class BaseEvasion:
    # add evasion class name inside the exception
    ADD_CLASS_NAME = True

    def fail_call_tokens(self):
        return [
            (NAME, "raise"),
            (NAME, "Exception"),
            (LPAR, "("),
            (
                STRING,
                repr(self.__class__.__name__)
                if self.ADD_CLASS_NAME
                else repr("evasion check triggered"),
            ),
            (RPAR, ")"),
        ]

    def import_tokens(self):
        return []

    def check_tokens(self):
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

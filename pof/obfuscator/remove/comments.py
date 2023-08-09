from tokenize import COMMENT, DEDENT, ENCODING, INDENT, NEWLINE, NL, STRING


class CommentsObfuscator:
    """Remove comments and docstrings from the code."""

    @staticmethod
    def obfuscate_tokens(tokens):
        result = []  # obfuscated tokens
        prev_toknum = None
        head = True  # to detect file docstrings
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            if toknum == STRING and (
                prev_toknum
                in [
                    NEWLINE,
                    DEDENT,
                    INDENT,
                    ENCODING,
                ]
                or head
            ):
                # Docstring
                new_tokens = None
            elif toknum == COMMENT:
                new_tokens = None

            if head and toknum not in [NEWLINE, NL, STRING, COMMENT]:
                head = False

            if new_tokens:
                result.extend(new_tokens)
            prev_toknum = toknum
        return result

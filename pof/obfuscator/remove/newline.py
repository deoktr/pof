from tokenize import INDENT, NEWLINE, NL


class NewlineObfuscator:
    """Remove empty lines."""

    @staticmethod
    def obfuscate_tokens(tokens):
        result = []  # obfuscated tokens
        prev_toknum = None
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            # remove empty lines from the original source
            # remove empty lines created after token manipulations
            # \n after \n --> 2 new lines in a row = one is useless
            # \n after NL --> same ^
            # \n after INDENT --> docstrings are placed after an indent
            if toknum == NL or (
                toknum == NEWLINE and (prev_toknum in (NEWLINE, NL, INDENT))
            ):
                new_tokens = None

            if new_tokens:
                result.extend(new_tokens)
            prev_toknum = toknum
        return result

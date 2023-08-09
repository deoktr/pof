# this could cause some problems, if the print statement was the
# only one present in the file
from tokenize import NAME, OP


class PrintObfuscator:
    """Remove print statements from the code."""

    @staticmethod
    def obfuscate_tokens(tokens):
        result = []  # obfuscated tokens
        parenthesis_depth = 0  # parenthesis depth
        prev_tokval = None
        print_par_depth = 0
        inside_print = False
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            if not inside_print and toknum == NAME and tokval == "print":
                new_tokens = None
                inside_print = True
                print_par_depth = parenthesis_depth

            if inside_print:
                if print_par_depth == parenthesis_depth and (
                    tokval not in ("(", "print") and prev_tokval != "print"
                ):  # check if still inside print
                    inside_print = False
                else:
                    new_tokens = None

            if toknum == OP and tokval == "(":
                parenthesis_depth += 1
            elif toknum == OP and tokval == ")":
                parenthesis_depth -= 1

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval
        return result

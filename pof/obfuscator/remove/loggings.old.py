from tokenize import NAME, OP


class LoggingObfuscator:
    """Remove logging statements from the code."""

    @staticmethod
    def obfuscate_tokens(tokens):
        result = []  # obfuscated tokens
        parenthesis_depth = 0  # parenthesis depth
        prev_tokval = None
        logging_par_depth = 0
        inside_log = False
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _, next_tokval, *__ = tokens[index + 1]

            if not inside_log and toknum == NAME and tokval == "logging":
                new_tokens = None
                inside_log = True
                logging_par_depth = parenthesis_depth

            if tokval == "import" and next_tokval == "logging":
                new_tokens = None

            if inside_log:
                if logging_par_depth == parenthesis_depth and (
                    tokval not in ("(", "logging")
                    and prev_tokval not in (".", "logging")
                ):  # check if still inside log
                    inside_log = False
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

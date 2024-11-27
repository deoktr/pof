from tokenize import NAME, OP, STRING


# TODO (deoktr): REFACTORING this class
class LoggingObfuscator:
    """Keep logging and change them with a generated code."""

    def __init__(self, add_codes=None, generator=None) -> None:
        if add_codes is None and generator is not None:
            add_codes = True
        self.add_codes = add_codes
        self.generator = generator

    def obfuscate_tokens(self, tokens):
        result = []  # obfuscated tokens
        parenthesis_depth = 0  # parenthesis depth
        prev_tokval = None
        logging_par_depth = 0
        inside_log = False
        logging_type = None
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _, next_tokval, *__ = tokens[index + 1]

            if toknum == OP and tokval == "(":
                parenthesis_depth += 1
            elif toknum == OP and tokval == ")":
                parenthesis_depth -= 1

            if inside_log:
                if (
                    logging_par_depth is not None
                    and parenthesis_depth < logging_par_depth
                    and tokval not in ["debug", "warning", "info", "critical", "error"]
                ):
                    inside_log = False

                    code = ""
                    if self.add_codes:
                        code = next(self.generator)

                    new_tokens = [
                        (NAME, logging_type),
                        (OP, "("),
                        (STRING, repr(code)),
                        (OP, ")"),
                    ]
                    logging_type = None
                else:
                    new_tokens = None

            elif (
                toknum == OP
                and tokval == "."
                and prev_tokval == "logging"
                and next_tokval in ["debug", "warning", "info", "critical", "error"]
            ):
                inside_log = True
                logging_type = next_tokval
                logging_par_depth = parenthesis_depth + 1

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval
        return result


class LoggingRemoveObfuscator:
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

            if toknum == OP and tokval == "(":
                parenthesis_depth += 1
            elif toknum == OP and tokval == ")":
                parenthesis_depth -= 1

            if inside_log:
                if (
                    logging_par_depth is not None
                    and parenthesis_depth <= logging_par_depth
                    and tokval not in ["debug", "warning", "info", "critical", "error"]
                    and tokval != ")"
                ):
                    inside_log = False
                    # replace logging statements with "pass"
                    new_tokens = [(NAME, "pass"), *new_tokens]
                else:
                    new_tokens = None

            elif (
                toknum == OP
                and tokval == "."
                and prev_tokval == "logging"
                and next_tokval in ["debug", "warning", "info", "critical", "error"]
            ):
                inside_log = True
                logging_par_depth = parenthesis_depth

                new_tokens = None
                # remove the last items "logging"
                result.pop()

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval
        return result

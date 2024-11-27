# TODO (deoktr): add parameter to disable spacing imports
import random
from tokenize import DEDENT, INDENT, NEWLINE


class AddNewlinesObfuscator:
    """Add newlines to the code."""

    def __init__(self, frequency=0.03) -> None:
        self.frequency = frequency

    def obfuscate_tokens(self, tokens):
        result = []  # obfuscated tokens
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]

            if toknum in [NEWLINE, INDENT, DEDENT]:
                if (random.randint(0, 100) / 100) <= self.frequency:
                    new_tokens.extend([(NEWLINE, "\n")])

                else:
                    # FIXME (deoktr): add newlines BEFORE class/function decorators
                    next_non_indent_tokval = None
                    for i in range(index, len(tokens)):
                        tn, tv, *__ = tokens[i]
                        if tn not in [NEWLINE, INDENT, DEDENT]:
                            next_non_indent_tokval = tv
                            break

                    if next_non_indent_tokval in ["def", "class"]:
                        # add a newline before
                        new_tokens = [(NEWLINE, "\n"), *new_tokens]

            if new_tokens:
                result.extend(new_tokens)
        return result

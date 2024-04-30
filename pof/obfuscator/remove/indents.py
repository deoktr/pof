# TODO (deoktr): support multi symbols indents (mix spaces and tabs)
# this might be extremly difficult because we'll have to keep track of the
# current function/class declaration, we can't mix inside the same function be
# between multiple we can
from tokenize import DEDENT, INDENT


class IndentsObfuscator:
    """Remove indents to minimum."""

    def __init__(self, indent=" ") -> None:
        self.indent = indent

    def obfuscate_tokens(self, tokens):
        result = []  # obfuscated tokens
        depth = 0  # indent depth
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            if toknum == INDENT:
                depth += 1
                new_tokens = [(toknum, depth * self.indent)]
            elif toknum == DEDENT:
                depth -= 1

            if new_tokens:
                result.extend(new_tokens)
        return result

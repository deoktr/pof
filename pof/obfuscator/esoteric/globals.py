import keyword
from tokenize import LPAR, NAME, OP, RPAR, STRING


# TODO (deoktr): add frequency
class GlobalsObfuscator:
    """Change a local function/class reference.

    ```
    def aaa():
        print(...)
    aaa()
    ```

    Would become:
    ```
    def aaa():
        print(...)
    globals()['aaa']()
    ```
    """

    RESERVED = keyword.kwlist

    @classmethod
    def obfuscate_tokens(cls, tokens):
        local_functions = []
        prev_tokval = None
        for toknum, tokval, *_ in tokens:
            if prev_tokval in ["def", "class"] and toknum == NAME:
                local_functions.append(tokval)
            prev_tokval = tokval

        result = []  # obfuscated tokens
        prev_tokval = None
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _, next_tokval, *__ = tokens[index + 1]

            if (
                tokval in local_functions
                # ensure it's not a definition
                and prev_tokval not in ["def", "class", "."]
                # ensure it's not an argument of a call
                and next_tokval not in ["="]
                and tokval not in cls.RESERVED
            ):
                new_tokens = [
                    (NAME, "globals"),
                    (LPAR, "("),
                    (RPAR, ")"),
                    (OP, "["),
                    (STRING, repr(tokval)),
                    (OP, "]"),
                ]

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval
        return result

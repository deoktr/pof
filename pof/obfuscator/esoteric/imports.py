from tokenize import LPAR, NAME, NEWLINE, OP, RPAR, STRING


class ImportsObfuscator:
    """Change a local function/class reference.

    ```
    import pathlib
    ```

    Would become:
    ```
    pathlib = __import__("pathlib")
    ```

    Note that this has not been tested very well.
    """

    @classmethod
    def obfuscate_tokens(cls, tokens):
        skip_next = False
        result = []  # obfuscated tokens
        prev_toknum = None
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _, next_tokval, *__ = tokens[index + 1]
            next_next_toknum = None
            if len(tokens) > index + 2:
                next_next_toknum, _, *__ = tokens[index + 2]

            if not skip_next:
                if (
                    tokval == "import"
                    and prev_toknum in [None, NEWLINE]
                    and next_next_toknum == NEWLINE
                ):
                    new_tokens = [
                        (NAME, next_tokval),
                        (OP, "="),
                        (NAME, "__import__"),
                        (LPAR, "("),
                        (STRING, repr(next_tokval)),
                        (RPAR, ")"),
                    ]
                    skip_next = True
            else:
                new_tokens = []
                skip_next = False

            if new_tokens:
                result.extend(new_tokens)
            prev_toknum = toknum
        return result

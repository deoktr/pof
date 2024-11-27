import keyword
from tokenize import NAME, OP


# TODO (deoktr): add frequency
class CallObfuscator:
    """Add `.__call__` to any call.

    ```
    print(...)
    ```

    ```
    print.__call__(...)
    ```
    """

    RESERVED_WORDS = ("type",)  # weir but if you do `type.__call__(1)` it doesn't work

    RESERVED = RESERVED_WORDS + tuple(keyword.kwlist)

    @classmethod
    def obfuscate_tokens(cls, tokens):
        result = []  # obfuscated tokens
        prev_tokval = None
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _, next_tokval, *__ = tokens[index + 1]

            if (
                # ensure it's not a definition
                (prev_tokval is None or prev_tokval not in ["def", "class"])
                and toknum == NAME
                and tokval not in cls.RESERVED
                and next_tokval == "("
            ):
                new_tokens.extend(
                    [
                        (OP, "."),
                        (NAME, "__call__"),
                    ],
                )

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval
        return result

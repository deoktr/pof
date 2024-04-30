# TODO (deoktr): work with f"" strings, r"" strings etc.
# TODO (deoktr): can't split `\` !!!
# TODO (deoktr): add variable to import or not b64decode
# TODO (deoktr): replace eval with ast.literal_eval: https://beta.ruff.rs/docs/rules/suspicious-eval-usage/

import logging
import random
from base64 import b64encode, b85encode
from enum import Enum
from tokenize import (
    DEDENT,
    ENCODING,
    INDENT,
    LPAR,
    NAME,
    NEWLINE,
    NUMBER,
    OP,
    RPAR,
    STRING,
)

from pof.errors import PofError
from pof.utils.cipher import ShiftCipher
from pof.utils.generator import AdvancedGenerator


class StringsObfuscator:
    """Obfuscate strings."""

    class Strats(Enum):
        BASE64 = 1
        ADDITION = 2  # FIXME (204): doesn't seems to work <
        ONLY_ADDITION = 3
        BASE85 = 4
        UNICODE = 5
        SHIFT = 6
        REPLACE = 7
        REVERSE = 8

    ALL = (
        Strats.BASE64,
        Strats.BASE85,
        Strats.SHIFT,
        Strats.REPLACE,
        Strats.REVERSE,
    )

    def __init__(  # noqa: PLR0913
        self,
        shift_cipher_class_obj=None,
        b64decode_name: str = "b64decode",
        b85decode_name: str = "b85decode",
        *,
        import_b64decode: bool = False,
        import_b85decode: bool = False,
    ) -> None:
        self.import_b64decode = import_b64decode
        self.import_b85decode = import_b85decode

        self.b64decode_name = b64decode_name
        self.b85decode_name = b85decode_name

        if shift_cipher_class_obj is None:
            shift_cipher_class_obj = ShiftCipher()
        self.shift_cipher_class_obj = shift_cipher_class_obj

    def obf_shift(self, tokval: str):
        # TODO (204): choose random padding here
        raw_string = eval(tokval)  # noqa: S307 PGH001
        if isinstance(raw_string, bytes):
            raw_string = raw_string.decode()
        encoded = self.shift_cipher_class_obj.encode_tokens(raw_string)
        return self.shift_cipher_class_obj.decode_tokens(encoded)

    def obf_base64(self, tokval: str):
        """Obfuscate string with base64.

        ```
        b64decode(b'...').decode()
        ```
        """
        raw_string = eval(tokval)  # noqa: S307 PGH001
        if isinstance(raw_string, str):
            raw_string = raw_string.encode()
        b64encoded_string = b64encode(raw_string).decode()
        return [
            (NAME, self.b64decode_name),
            (LPAR, "("),
            (STRING, repr(b64encoded_string)),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "decode"),
            (LPAR, "("),
            (RPAR, ")"),
        ]

    def obf_base85(self, tokval: str):
        """Obfuscate string with base85.

        ````
        b85decode(b'...').decode()
        ````
        """
        raw_string = eval(tokval)  # noqa: S307 PGH001
        if isinstance(raw_string, str):
            raw_string = raw_string.encode()
        b85encoded_string = b85encode(raw_string).decode()
        return [
            (NAME, self.b85decode_name),
            (LPAR, "("),
            (STRING, repr(b85encoded_string)),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "decode"),
            (LPAR, "("),
            (RPAR, ")"),
        ]

    @staticmethod
    def unicode(tokval: str):
        # Hell --> \u0048\u0065\u006C\u006C
        raw_string = eval(tokval)  # noqa: S307 PGH001
        if isinstance(raw_string, bytes):
            raw_string = raw_string.decode()
        encoded = ""
        for c in raw_string:
            ucode = f"\\u{hex(ord(c))[2:]:0>4}" if not c.isdigit() else c
            encoded += ucode
        return [(STRING, f"'{encoded}'")]

    @staticmethod
    def additions(tokval: str):
        # "Hello, world!" --> "Hello, "+"world!"
        raw_string = False
        if tokval.startswith("r"):
            tokval = tokval[1:]
            raw_string = True

        symbols = tokval[-1]
        first_symbol = symbols
        if raw_string:
            first_symbol = "r" + first_symbol
        last_symbol = symbols
        s = random.randint(2, len(tokval) - 4)
        string_1 = first_symbol + tokval[1:s] + last_symbol
        string_2 = first_symbol + tokval[s:-1] + last_symbol
        return [
            (STRING, string_1),
            (OP, "+"),
            (STRING, string_2),
        ]

    @staticmethod
    def only_additions(tokval: str):
        # "Hello, world!" --> "Hello, "+"world!"
        raw_string = False
        if tokval.startswith("r"):
            tokval = tokval[1:]
            raw_string = True

        symbols = tokval[-1]
        first_symbol = symbols
        if raw_string:
            first_symbol = "r" + first_symbol
        last_symbol = symbols
        t = []
        add_slash = False
        for char in tokval[1:-1]:
            if char != "\\" and not add_slash:
                t.extend(
                    [
                        (STRING, first_symbol + char + last_symbol),
                        (OP, "+"),
                    ],
                )
            elif add_slash:
                t.extend(
                    [
                        (STRING, first_symbol + "\\" + char + last_symbol),
                        (OP, "+"),
                    ],
                )
                add_slash = False
            else:
                add_slash = True
        t.pop()  # remove last +
        return t

    @staticmethod
    def string_replace(tokval: str):
        raw_string = eval(tokval)  # noqa: S307 PGH001

        if not raw_string:
            return [(STRING, tokval)]

        i = random.randint(0, len(raw_string) - 1)
        j = random.randint(i + 1, len(raw_string))
        original = raw_string[i:j]

        # TODO (204): add option to change the generator
        generator = AdvancedGenerator.realistic_generator()
        new = next(generator)
        retries = 0
        max_retries = 5
        while new in raw_string:
            if retries >= max_retries:
                msg = "unable to generate a string that wasn't present in the original"
                raise PofError(msg)
            new = next(generator)
            retries += 1

        new_string = raw_string.replace(original, new)

        return [
            (STRING, repr(new_string)),
            (OP, "."),
            (NAME, "replace"),
            (OP, "("),
            (STRING, repr(new)),
            (OP, ","),
            (STRING, repr(original)),
            (OP, ")"),
        ]

    @staticmethod
    def string_reverse(tokval: str):
        raw_string = eval(tokval)  # noqa: S307 PGH001
        reversed_string = raw_string[::-1]
        return [
            (STRING, repr(reversed_string)),
            (OP, "["),
            (OP, ":"),
            (OP, ":"),
            (NUMBER, "-1"),
            (OP, "]"),
        ]

    def obfuscate_string(self, tokval: str, next_tokval: str):
        # TODO (204): consider f"" u"" ur"" b"" r"" strings
        # consider empty strings
        # consider calling function on whole string "".format()
        strategies = self.ALL  # list(self.Strats._value2member_map_.values())

        # if len(tokval) >= 6:
        #     strategies = strategies.copy()
        #     strategies.append(self.Strats.ADDITION)

        # if len(tokval) >= 6 and next_tokval != ".":
        #     strategies = strategies.copy()
        #     strategies.append(self.Strats.ONLY_ADDITION)

        if next_tokval != ".":
            strategies = list(strategies)
            strategies.extend(
                [
                    self.Strats.UNICODE,
                    self.Strats.SHIFT,
                ],
            )

        strategy = random.choice(strategies)

        if strategy == self.Strats.BASE64:
            tokens = self.obf_base64(tokval)
        elif strategy == self.Strats.ADDITION:
            tokens = self.additions(tokval)
        elif strategy == self.Strats.ONLY_ADDITION:
            tokens = self.only_additions(tokval)
        elif strategy == self.Strats.BASE85:
            tokens = self.obf_base85(tokval)
        elif strategy == self.Strats.UNICODE:
            tokens = self.unicode(tokval)
        elif strategy == self.Strats.SHIFT:
            tokens = self.obf_shift(tokval)
        elif strategy == self.Strats.REPLACE:
            tokens = self.string_replace(tokval)
        elif strategy == self.Strats.REVERSE:
            tokens = self.string_reverse(tokval)
        else:
            logging.error("funsupported {strategy}", extra={"strategy": strategy})
            return None

        return tokens

    def obfuscate_tokens(self, tokens):
        result = []  # obfuscated tokens

        if self.import_b64decode:
            if self.b64decode_name != "b64decode":
                result.extend(
                    [
                        (NAME, "from"),
                        (NAME, "base64"),
                        (NAME, "import"),
                        (NAME, "b64decode"),
                        (NAME, "as"),
                        (NAME, self.b64decode_name),
                        (NEWLINE, "\n"),
                    ],
                )
            else:
                result.extend(
                    [
                        (NAME, "from"),
                        (NAME, "base64"),
                        (NAME, "import"),
                        (NAME, "b64decode"),
                        (NEWLINE, "\n"),
                    ],
                )

        if self.import_b85decode:
            if self.b85decode_name != "b85decode":
                result.extend(
                    [
                        (NAME, "from"),
                        (NAME, "base64"),
                        (NAME, "import"),
                        (NAME, "b85decode"),
                        (NAME, "as"),
                        (NAME, self.b85decode_name),
                        (NEWLINE, "\n"),
                    ],
                )
            else:
                result.extend(
                    [
                        (NAME, "from"),
                        (NAME, "base64"),
                        (NAME, "import"),
                        (NAME, "b85decode"),
                        (NEWLINE, "\n"),
                    ],
                )

        prev_toknum = None
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _, next_tokval, *__ = tokens[index + 1]

            # don't obfuscate docstrings
            if toknum == STRING and prev_toknum not in [
                NEWLINE,
                DEDENT,
                INDENT,
                ENCODING,
            ]:
                try:
                    new_tokens = self.obfuscate_string(tokval, next_tokval)
                except Exception:
                    logging.exception()

            if new_tokens:
                result.extend(new_tokens)
            prev_toknum = toknum
        return result

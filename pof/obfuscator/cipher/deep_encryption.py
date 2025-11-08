# POF, a free and open source Python obfuscation framework.
# Copyright (C) 2022 - 2025  POF Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# FIXME (deoktr): work in progress !
from base64 import b64encode
from tokenize import DEDENT, INDENT, LPAR, NAME, NEWLINE, OP, RPAR, STRING, untokenize

from pof.logger import logger


class DeepEncryptionObfuscator:
    def __init__(self, encryption_depth=0) -> None:
        self.encryption_depth = encryption_depth

    def obfuscate_tokens(self, tokens):  # noqa: C901 PLR0912
        """Encrypt every function's source code.

        Encrypt every function's source code with different keys, and decrypt
        only when needed (just-in-time).
        This will prevent the entire source code being accessible at once in the
        memory, of course the draw back is the speed will be reduced.
        Also verify integrity dynamically, maybe also sign encrypted code.

        Convert functions into the following:

        ```
        def function():
            r_dict=globals().copy()
            r_dict.update(locals())
            exec(b64decode(b'base64functioncode...'), r_dict)
            if'r'not in r_dict:
                return None
            r_val=r_dict['r']
            del r_dict
            return r_val
        ```

        Todo:
        - create a function 'exec_return' and call it with en encrypted source
        """
        result = []  # obfuscated tokens
        # just for testing
        result.extend(
            [
                (NAME, "from"),
                (NAME, "base64"),
                (NAME, "import"),
                (NAME, "b64decode"),
                (NEWLINE, "\n"),
            ],
        )
        depth = 0  # indent depth
        function_tokens = []
        function_def = False
        inside_function = False
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _next_toknum, next_tokval, *__ = tokens[index + 1]

            if toknum == INDENT:
                depth += 1
            elif toknum == DEDENT:
                depth -= 1

            if inside_function:
                function_tokens.append((toknum, tokval))
                new_tokens = []

            if tokval == "def" and toknum == NAME and depth == self.encryption_depth:
                logger.debug("function definition: %s", next_tokval)
                function_def = True
            elif function_def and toknum == OP and tokval == ":":
                function_def = False
                inside_function = True
            elif (
                inside_function and depth <= self.encryption_depth and toknum == DEDENT
            ):
                inside_function = False
                # [2:-1] is to remove indent/dedent

                fixed_function_tokens = []
                # FIXME (deoktr): fix
                fixed_depth = -1  # should it be - (self.encryption_depth) ??
                for ftnum, ftval in function_tokens:
                    ftval_d = ftval
                    if ftnum == INDENT:
                        fixed_depth += 1
                        ftval_d = fixed_depth * "    "
                    elif ftnum == DEDENT:
                        fixed_depth -= 1
                    fixed_function_tokens.append((ftnum, ftval_d))

                # TODO (deoktr): need to change ALL indents tokens
                source = untokenize(fixed_function_tokens[2:-1])

                # obviously doesn't work with yield
                if not any(i in source for i in ["yield", "super"]):
                    # TODO (deoktr): find a way better way
                    # FIXME (deoktr): this should replace empty return statements
                    source = source.replace("return\n", "r=None")
                    source = source.replace("return", "r=")

                    encoded = b64encode(source.encode())
                    globals_dict_name = "r_dict"
                    new_tokens = [
                        (NEWLINE, "\n"),
                        (
                            INDENT,
                            "    " * (self.encryption_depth + 1),
                        ),  # TODO (deoktr): change me
                        (NAME, globals_dict_name),
                        (OP, "="),
                        (NAME, "globals"),
                        (LPAR, "("),
                        (LPAR, ")"),
                        (OP, "."),
                        (OP, "copy"),
                        (LPAR, "("),
                        (LPAR, ")"),
                        (NEWLINE, "\n"),
                        (NAME, globals_dict_name),
                        (OP, "."),
                        (NAME, "update"),
                        (LPAR, "("),
                        (NAME, "locals"),
                        (LPAR, "("),
                        (LPAR, ")"),
                        (LPAR, ")"),
                        (NEWLINE, "\n"),
                        # print the code before executing it, for testing
                        (NAME, "print"),
                        (LPAR, "("),
                        (NAME, "b64decode"),
                        (LPAR, "("),
                        (STRING, repr(encoded)),
                        (RPAR, ")"),
                        (OP, "."),
                        (NAME, "decode"),
                        (LPAR, "("),
                        (RPAR, ")"),
                        (RPAR, ")"),
                        (NEWLINE, "\n"),
                        (NAME, "exec"),
                        (LPAR, "("),
                        # just for testing
                        (NAME, "b64decode"),
                        (LPAR, "("),
                        (STRING, repr(encoded)),
                        (RPAR, ")"),
                        (OP, ","),
                        (NAME, globals_dict_name),
                        (RPAR, ")"),
                        (NEWLINE, "\n"),
                        (NAME, "if"),
                        (STRING, "'r'"),
                        (NAME, "not"),
                        (NAME, "in"),
                        (NAME, globals_dict_name),
                        (OP, ":"),
                        (NEWLINE, "\n"),
                        (
                            INDENT,
                            "    " * (self.encryption_depth + 2),
                        ),  # TODO (deoktr): change me
                        (NAME, "return"),
                        (NAME, "None"),
                        (DEDENT, ""),
                        (NEWLINE, "\n"),
                        (NAME, "r_val"),
                        (OP, "="),
                        (NAME, globals_dict_name),
                        (OP, "["),
                        (STRING, "'r'"),
                        (OP, "]"),
                        (NEWLINE, "\n"),
                        (NAME, "del"),
                        (NAME, globals_dict_name),
                        (NEWLINE, "\n"),
                        (NAME, "return"),
                        (NAME, "r_val"),
                        (NEWLINE, "\n"),
                        (DEDENT, ""),
                    ]
                else:
                    new_tokens = function_tokens.copy()

                function_tokens = []

            if new_tokens:
                result.extend(new_tokens)

        return result

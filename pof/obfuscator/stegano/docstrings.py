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

import ast
import io
from tokenize import LPAR, NAME, NEWLINE, OP, RPAR, STRING, generate_tokens

from pof.utils.encoding import Base64Encoding
from pof.utils.tokens import untokenize


class DocstringObfuscator:
    """Hide code inside doc strings."""

    # TODO (deoktr): add ability to choose entry point (function) name without calling
    # it put the exec code inside this function
    # TODO (deoktr): add ability to choose the base code
    # TODO (deoktr): add ability to split the docstring among multiple class/functions

    def __init__(self, encoding_class=None, base_code=None) -> None:
        if encoding_class is None:
            encoding_class = Base64Encoding
        self.encoding_class = encoding_class

        if base_code is None:
            base_code = "class Foo:\n    pass\n"
        self.base_code = base_code

    def get_exec_tokens(self, name):
        # the replace will remove \n and space indents from the docstrings
        # because on some encoding it can break it, it works without problems
        # with base64 but doesn't with base85, base16 and other.
        docstring_tokens = [
            (NAME, name),
            (OP, "."),
            (NAME, "__doc__"),
            (OP, "."),
            (NAME, "replace"),
            (LPAR, "("),
            (STRING, repr(r"\n")),
            (OP, ","),
            (STRING, "''"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "replace"),
            (LPAR, "("),
            (STRING, repr(" ")),
            (OP, ","),
            (STRING, repr("")),
            (RPAR, ")"),
        ]
        return [
            (NEWLINE, "\n"),
            (NAME, "exec"),
            (LPAR, "("),
            *self.encoding_class.decode_tokens(docstring_tokens),
            (RPAR, ")"),
        ]

    def get_docstring(self, code, indent="    "):
        encode_tokens = ast.literal_eval(
            untokenize(self.encoding_class.encode_tokens(code.encode())),
        )

        docstring = "\n" + indent
        chunk_size = 74
        for i in range(0, len(encode_tokens), chunk_size):
            chunk = encode_tokens[i : i + chunk_size]
            docstring += chunk + "\n" + indent
        return f'"""{docstring}"""'

    def get_base_tokens(self):
        io_obj = io.StringIO(self.base_code)
        return list(generate_tokens(io_obj.readline))

    def obfuscate_tokens(self, tokens):
        code = untokenize(tokens)
        docstring = self.get_docstring(code)

        base_tokens = self.get_base_tokens()

        in_declaration = False
        prev_tokval = None
        name = None
        new_tokens = []
        add_next = False
        for toknum, tokval, *_ in base_tokens:
            tokens = [(toknum, tokval)]

            if add_next:
                tokens.extend([(STRING, docstring), (NEWLINE, "\n")])
                add_next = False

            # and name is None : used to add the docstring on only one
            # class/function definition
            # FIXME (deoktr): split it among multiple definitions
            if prev_tokval in ["def", "class"] and name is None:
                name = tokval
                in_declaration = True
            elif prev_tokval == ":" and in_declaration:
                add_next = True
                in_declaration = False

            prev_tokval = tokval
            new_tokens.extend(tokens)

        return [
            *self.encoding_class.import_tokens(),
            (NEWLINE, "\n"),
            *new_tokens,
            (NEWLINE, "\n"),
            *self.get_exec_tokens(name),
            (NEWLINE, "\n"),
        ]

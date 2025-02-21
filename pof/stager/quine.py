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

"""Quine generator."""

# TODO (deoktr): add opttion to keep the source code, and simply add the quine function
# this has the advantage of not using `exec` but the disadvantage of having a
# much heavier file (around double) because we store the source AND the
# encrypted encoded esource
# TODO (deoktr): have another way to store the base64 code, for example in the comments
# using the other stagers. Or even have the original code still present, and hide the
# quine 'source' inside the comments, and have the quine function hidden.

import io
from tokenize import (
    DEDENT,
    INDENT,
    NAME,
    NEWLINE,
    NUMBER,
    OP,
    generate_tokens,
    untokenize,
)

from pof.utils.encoding import Base64Encoding


class QuineStager:
    """Add quine.

    This allow the call of the `quine` function, to output the current source
    code. This is extremely useful to spread, and can even be combined with an
    obfuscator script to change every times it propagate.
    """

    def __init__(self, encoding_class=None, quine_function_name="quine") -> None:
        # TODO (deoktr): include generator to generate var names
        # is this really a good idea ? if we can use the obfuscator function to
        # do the job
        if encoding_class is None:
            encoding_class = Base64Encoding
        self.encoding_class = encoding_class
        self.quine_function_name = quine_function_name

    def generate_stager(self, tokens):
        code = untokenize(tokens).encode()
        esource = self.encoding_class.encode_tokens(code)
        import_tokens = self.encoding_class.import_tokens()

        quine_tokens_1 = [
            *import_tokens,
            (NEWLINE, "\n"),
            (NAME, "from"),
            (NAME, "tokenize"),
            (NAME, "import"),
            (NAME, "untokenize"),
            (NEWLINE, "\n"),
            (NAME, "esource"),
            (OP, "="),
            # place base64 source here
        ]

        quine_tokens_2 = [
            (NEWLINE, "\n"),
            (NAME, "tokens"),
            (OP, "="),
            # place quine tokens list here
        ]

        quine_tokens_3 = [
            (NEWLINE, "\n"),
            (NAME, "def"),
            (NAME, self.quine_function_name),
            (OP, "("),
            (OP, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, " "),
            (NAME, "return"),
            (NAME, "untokenize"),
            (OP, "("),
            (NAME, "tokens"),
            (OP, "["),
            (OP, ":"),
            (NUMBER, "12"),
            (OP, "]"),
            (OP, ")"),
            (OP, "+"),
            (NAME, "repr"),
            (OP, "("),
            (NAME, "esource"),
            (OP, ")"),
            (OP, "+"),
            (NAME, "untokenize"),
            (OP, "("),
            (NAME, "tokens"),
            (OP, "["),
            (NUMBER, "12"),
            (OP, ":"),
            (NUMBER, "15"),
            (OP, "]"),
            (OP, ")"),
            (OP, "+"),
            (NAME, "repr"),
            (OP, "("),
            (NAME, "tokens"),
            (OP, ")"),
            (OP, "+"),
            (NAME, "untokenize"),
            (OP, "("),
            (NAME, "tokens"),
            (OP, "["),
            (NUMBER, "15"),
            (OP, ":"),
            (OP, "]"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            (NAME, "exec"),
            (OP, "("),
            *self.encoding_class.decode_tokens([(NAME, "esource")]),
            (OP, ")"),
            (NEWLINE, "\n"),
        ]

        # generate the tokens of the tokens list
        quine_tokens = repr(quine_tokens_1 + quine_tokens_2 + quine_tokens_3)
        io_obj = io.StringIO(quine_tokens)
        source_tokens = list(generate_tokens(io_obj.readline))

        return [
            *quine_tokens_1,
            *esource,
            *quine_tokens_2,
            *source_tokens,
            *quine_tokens_3,
        ]

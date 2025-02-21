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

from tokenize import LPAR, NAME, NEWLINE, OP, RPAR, STRING


class ImportsObfuscator:
    """Obfuscate the import statement.

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

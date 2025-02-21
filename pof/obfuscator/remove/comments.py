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

from tokenize import COMMENT, DEDENT, ENCODING, INDENT, NEWLINE, NL, STRING


class CommentsObfuscator:
    """Remove comments and docstrings from the code."""

    @staticmethod
    def obfuscate_tokens(tokens):
        result = []  # obfuscated tokens
        prev_toknum = None
        head = True  # to detect file docstrings
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            if toknum == STRING and (
                prev_toknum
                in [
                    NEWLINE,
                    DEDENT,
                    INDENT,
                    ENCODING,
                ]
                or head
            ):
                # Docstring
                new_tokens = None
            elif toknum == COMMENT:
                new_tokens = None

            if head and toknum not in [NEWLINE, NL, STRING, COMMENT]:
                head = False

            if new_tokens:
                result.extend(new_tokens)
            prev_toknum = toknum
        return result

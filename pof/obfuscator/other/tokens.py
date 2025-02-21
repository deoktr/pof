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

from tokenize import LPAR, NAME, NEWLINE, NUMBER, OP, RPAR, STRING


class TokensObfuscator:
    """Store tokens, and untokenize to exec at runtime."""

    @staticmethod
    def import_tokens():
        return [
            (NAME, "from"),
            (NAME, "tokenize"),
            (NAME, "import"),
            (NAME, "untokenize"),
        ]

    @staticmethod
    def generate_tokens_list(tokens):
        tokens_list = []
        tokens_list.append((OP, "["))
        for toknum, tokval, *_ in tokens:
            tokens_list.extend(
                [
                    (LPAR, "("),
                    (NUMBER, str(toknum)),
                    (OP, ","),
                    (STRING, repr(tokval)),
                    (RPAR, ")"),
                    (OP, ","),
                ],
            )
        tokens_list.append((OP, "]"))
        return tokens_list

    @classmethod
    def obfuscate_tokens(cls, tokens):
        return [
            *cls.import_tokens(),
            (NEWLINE, "\n"),
            (NAME, "exec"),
            (LPAR, "("),
            (NAME, "untokenize"),
            (LPAR, "("),
            *cls.generate_tokens_list(tokens),
            (RPAR, ")"),
            (RPAR, ")"),
            (NEWLINE, "\n"),
        ]

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

from tokenize import DEDENT, INDENT, LPAR, NAME, NEWLINE, OP, RPAR, STRING


class BaseEvasion:
    # add evasion class name inside the exception
    ADD_CLASS_NAME = True

    @classmethod
    def fail_call_tokens(cls):
        return [
            (NAME, "raise"),
            (NAME, "Exception"),
            (LPAR, "("),
            (
                STRING,
                (
                    repr(cls.__class__.__name__)
                    if cls.ADD_CLASS_NAME
                    else repr("evasion check triggered")
                ),
            ),
            (RPAR, ")"),
        ]

    @staticmethod
    def import_tokens():
        return []

    @staticmethod
    def check_tokens():
        return []

    def add_evasion(self, tokens):
        return [
            *self.import_tokens(),
            (NEWLINE, "\n"),
            (NAME, "if"),
            (LPAR, "("),
            *self.check_tokens(),
            (RPAR, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "    "),
            *self.fail_call_tokens(),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            *tokens,
        ]

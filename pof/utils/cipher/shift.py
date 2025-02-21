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

from tokenize import LPAR, NAME, NUMBER, OP, RPAR, STRING


class ShiftCipher:
    """Shift/Caesar cipher."""

    def __init__(self, padding=3) -> None:
        self.padding = padding

    @staticmethod
    def import_tokens():
        return []

    def encode_tokens(self, string):
        cipher = "".join([chr(ord(i) + self.padding) for i in string])
        return [(STRING, repr(cipher))]

    def decode_tokens(self, encoded_tokens):
        """`"".join([chr(ord(i)-3) for i in "Khoor/#Zruog$"])`."""
        return [
            (STRING, '""'),
            (OP, "."),
            (NAME, "join"),
            (LPAR, "("),
            (OP, "["),
            (NAME, "chr"),
            (LPAR, "("),
            (NAME, "ord"),
            (LPAR, "("),
            (NAME, "i"),
            (RPAR, ")"),
            (OP, "-"),
            (NUMBER, str(self.padding)),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "i"),
            (NAME, "in"),
            *encoded_tokens,
            (OP, "]"),
            (RPAR, ")"),
        ]

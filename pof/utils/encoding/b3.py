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

from tokenize import DEDENT, INDENT, LPAR, NAME, NEWLINE, NUMBER, OP, RPAR, STRING


# TODO (deoktr): add 2 way of doing the encoding, one (the current) where you need the
# function at the top of the file, and another where it's inline, so there would
# be no need for a function definition
class Base3Encoding:
    """Base 3 is a troll integer encoding.

    The only goal of this encoding is have numbers has strings and composed only
    of `0oO` only 'round' symbols.
    """

    @staticmethod
    def encode(number: int):
        """Converts an integer to a base3 string."""
        if not isinstance(number, int):
            msg = "number must be an integer"
            raise TypeError(msg)

        alphabet = "0oO"

        base3 = ""
        sign = ""

        if number < 0:
            sign = "-"
            number = -number

        if 0 <= number < len(alphabet):
            return sign + alphabet[number]

        while number != 0:
            number, i = divmod(number, len(alphabet))
            base3 = alphabet[i] + base3

        return sign + base3

    @classmethod
    def encode_tokens(cls, number: int):
        return [(STRING, repr(cls.encode(number)))]

    @staticmethod
    def definition_tokens():
        """Base 3 decode function definition tokens.

        ```
        def b3decode(number):
            return int(number.replace("o", "1").replace("O", "2"), 3)
        ```.
        """
        return [
            (NAME, "def"),
            (NAME, "b3decode"),
            (OP, "("),
            (NAME, "number"),
            (OP, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "    "),
            (NAME, "return"),
            (NAME, "int"),
            (OP, "("),
            (NAME, "number"),
            (OP, "."),
            (NAME, "replace"),
            (OP, "("),
            (STRING, repr("o")),
            (OP, ","),
            (STRING, repr("1")),
            (OP, ")"),
            (OP, "."),
            (NAME, "replace"),
            (OP, "("),
            (STRING, repr("O")),
            (OP, ","),
            (STRING, repr("2")),
            (OP, ")"),
            (OP, ","),
            (NUMBER, "3"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
        ]

    @staticmethod
    def decode_tokens(encoded_tokens):
        return [
            (NAME, "b3decode"),
            (LPAR, "("),
            *encoded_tokens,
            (RPAR, ")"),
        ]

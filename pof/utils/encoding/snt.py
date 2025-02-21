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


class SpacenTabEncoding:
    r"""Space and tab encoding.

    Encode 0 as a space ( ), 1 as a tab (\t).
    """

    @staticmethod
    def encode(string):
        string_bin = bin(int.from_bytes(string, "big")).replace("0b", "")
        out = ""
        for bit in string_bin:
            if bit == "0":
                out += " "
            elif bit == "1":
                out += "\t"
        return out

    @classmethod
    def encode_tokens(cls, string):
        return [(STRING, repr(cls.encode(string)))]

    @staticmethod
    def import_tokens():
        return []

    @classmethod
    def definition_tokens(cls):
        return [
            (NAME, "def"),
            (NAME, "sntdecode"),
            (OP, "("),
            (NAME, "encoded"),
            (OP, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "    "),
            (NAME, "msg_bin"),
            (OP, "="),
            (NAME, "encoded"),
            (OP, "."),
            (NAME, "replace"),
            (OP, "("),
            (STRING, '" "'),
            (OP, ","),
            (STRING, '"0"'),
            (OP, ")"),
            (OP, "."),
            (NAME, "replace"),
            (OP, "("),
            (STRING, '"\\t"'),
            (OP, ","),
            (STRING, '"1"'),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "n"),
            (OP, "="),
            (NAME, "int"),
            (OP, "("),
            (NAME, "msg_bin"),
            (OP, ","),
            (NUMBER, "2"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "return"),
            (NAME, "n"),
            (OP, "."),
            (NAME, "to_bytes"),
            (OP, "("),
            (OP, "("),
            (NAME, "n"),
            (OP, "."),
            (NAME, "bit_length"),
            (OP, "("),
            (OP, ")"),
            (OP, "+"),
            (NUMBER, "7"),
            (OP, ")"),
            (OP, "//"),
            (NUMBER, "8"),
            (OP, ","),
            (STRING, '"big"'),
            (OP, ")"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
        ]

    @staticmethod
    def decode_tokens(encoded_tokens):
        return [
            (NAME, "sntdecode"),
            (LPAR, "("),
            *encoded_tokens,
            (RPAR, ")"),
        ]

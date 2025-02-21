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

import gzip
import marshal
from tokenize import COMMA, LPAR, NAME, OP, RPAR, STRING


class GzipCompression:
    @staticmethod
    def encode(string):
        return gzip.compress(marshal.dumps(string))

    @classmethod
    def encode_tokens(cls, string):
        return [(STRING, repr(cls.encode(string)))]

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "gzip"),
            (COMMA, ","),
            (NAME, "marshal"),
        ]

    @staticmethod
    def decode_tokens(encoded_tokens):
        return [
            (NAME, "marshal"),
            (OP, "."),
            (NAME, "loads"),
            (LPAR, "("),
            (NAME, "gzip"),
            (OP, "."),
            (NAME, "decompress"),
            (LPAR, "("),
            *encoded_tokens,
            (RPAR, ")"),
            (RPAR, ")"),
        ]

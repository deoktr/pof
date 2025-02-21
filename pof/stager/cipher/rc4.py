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

from tokenize import LPAR, NAME, NEWLINE, NUMBER, OP, RPAR

from pof.utils.cipher import RC4Cipher
from pof.utils.tokens import untokenize


class RC4Stager(RC4Cipher):
    """Takes the key as first argument to decrypt and execute."""

    def generate_stager(self, tokens):
        code = untokenize(tokens)
        key_tokens = [
            (NAME, "sys"),
            (OP, "."),
            (NAME, "argv"),
            (OP, "."),
            (NAME, "pop"),
            (OP, "("),
            (NUMBER, "1"),
            (OP, ")"),
        ]

        return [
            (NAME, "import"),
            (NAME, "sys"),
            (NEWLINE, "\n"),
            *self.import_tokens(),
            (NEWLINE, "\n"),
            *self.definition_tokens(),
            (NEWLINE, "\n"),
            (NAME, "exec"),
            (LPAR, "("),
            *self.decode_tokens(self.encode_tokens(code), key_tokens=key_tokens),
            (RPAR, ")"),
            (NEWLINE, "\n"),
        ]

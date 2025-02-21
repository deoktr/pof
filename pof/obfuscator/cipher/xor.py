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

"""This is not a secure encryption method!

The main purpose of xor is to produce radically different outputs when obfuscating a
file.
"""

import random
from base64 import b64encode
from tokenize import DEDENT, INDENT, NAME, NEWLINE, NL, NUMBER, OP, STRING

from pof.utils.tokens import untokenize


class XORObfuscator:
    """XOR obfuscator."""

    # TODO (deoktr): move code to utils/encryption/xor.py
    @staticmethod
    def get_exec_tokens(key, ciphertext):
        return [
            [NAME, "from"],
            [NAME, "base64"],
            [NAME, "import"],
            [NAME, "b64decode"],
            [NEWLINE, "\n"],
            [NL, "\n"],
            [NAME, "def"],
            [NAME, "decrypt"],
            [OP, "("],
            [NAME, "cipher"],
            [OP, ","],
            [NAME, "key"],
            [OP, ")"],
            [OP, ":"],
            [NEWLINE, "\n"],
            [INDENT, "    "],
            [NAME, "bcipher"],
            [OP, "="],
            [NAME, "bytearray"],
            [OP, "("],
            [NAME, "b64decode"],
            [OP, "("],
            [NAME, "cipher"],
            [OP, ")"],
            [OP, ")"],
            [NEWLINE, "\n"],
            [NAME, "text"],
            [OP, "="],
            [NAME, "bytearray"],
            [OP, "("],
            [OP, ")"],
            [NEWLINE, "\n"],
            [NAME, "ki"],
            [OP, "="],
            [NUMBER, "0"],
            [NEWLINE, "\n"],
            [NAME, "for"],
            [NAME, "i"],
            [NAME, "in"],
            [NAME, "bcipher"],
            [OP, ":"],
            [NEWLINE, "\n"],
            [INDENT, "        "],
            [NAME, "text"],
            [OP, "."],
            [NAME, "append"],
            [OP, "("],
            [NAME, "i"],
            [OP, "^"],
            [NAME, "key"],
            [OP, "["],
            [NAME, "ki"],
            [OP, "%"],
            [NAME, "len"],
            [OP, "("],
            [NAME, "key"],
            [OP, ")"],
            [OP, "]"],
            [OP, ")"],
            [NEWLINE, "\n"],
            [NAME, "ki"],
            [OP, "+="],
            [NUMBER, "1"],
            [NEWLINE, "\n"],
            [DEDENT, ""],
            [NAME, "return"],
            [NAME, "text"],
            [NEWLINE, "\n"],
            [DEDENT, ""],
            [NAME, "exec"],
            [OP, "("],
            [NAME, "decrypt"],
            [OP, "("],
            [STRING, repr(ciphertext)],
            [OP, ","],
            [STRING, repr(key)],
            [OP, ")"],
            [OP, "."],
            [NAME, "decode"],
            [OP, "("],
            [OP, ")"],
            [OP, ")"],
            [NEWLINE, "\n"],
        ]

    @staticmethod
    def encrypt_code(text, key):
        bcipher = bytearray()
        for ki, i in enumerate(text):
            bcipher.append(i ^ key[ki % len(key)])
        return b64encode(bcipher)

    def obfuscate_tokens(self, tokens, key: str | None = None):
        code = untokenize(tokens).encode()
        if key is None:
            key = str(random.randint(0, 100000000)).encode()
        ciphertext = self.encrypt_code(code, key)
        return self.get_exec_tokens(
            key=key,
            ciphertext=ciphertext,
        )

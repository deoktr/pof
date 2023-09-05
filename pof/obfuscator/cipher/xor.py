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

    # TODO (204): move code to utils/encryption/xor.py
    def get_exec_tokens(self, key, ciphertext):
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

    def encrypt_code(self, text, key):
        bcipher = bytearray()
        ki = 0
        for i in text:
            bcipher.append(i ^ key[ki % len(key)])
            ki += 1
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

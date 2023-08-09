from tokenize import DEDENT, INDENT, LPAR, NAME, NEWLINE, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class IntegrityEvasion(BaseEvasion):
    def import_tokens(self):
        return [
            (NAME, "import"),
            (NAME, "hashlib"),
            (OP, ","),
            (NAME, "inspect"),
        ]

    def integrity_function_tokens(self):
        """Integrity check tokens.

        ```
        def integrity(ihash):
            stack = ""
            for obj in [integrity]:
                stack += inspect.getsource(obj)
            m = hashlib.sha3_512()
            m.update(stack.encode())
            m.digest()
            h = m.hexdigest()
            return h != ihash
        # code...
        ```
        """
        return [
            (NAME, "def"),
            (NAME, "integrity"),
            (OP, "("),
            (NAME, "ihash"),
            (OP, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "    "),
            (NAME, "stack"),
            (OP, "="),
            (STRING, '""'),
            (NEWLINE, "\n"),
            (NAME, "for"),
            (NAME, "obj"),
            (NAME, "in"),
            (OP, "["),
            (NAME, "integrity"),
            (OP, "]"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "        "),
            (NAME, "stack"),
            (OP, "+="),
            (NAME, "inspect"),
            (OP, "."),
            (NAME, "getsource"),
            (OP, "("),
            (NAME, "obj"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            (NAME, "m"),
            (OP, "="),
            (NAME, "hashlib"),
            (OP, "."),
            (NAME, "sha3_512"),
            (OP, "("),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "m"),
            (OP, "."),
            (NAME, "update"),
            (OP, "("),
            (NAME, "stack"),
            (OP, "."),
            (NAME, "encode"),
            (OP, "("),
            (OP, ")"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "m"),
            (OP, "."),
            (NAME, "digest"),
            (OP, "("),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "h"),
            (OP, "="),
            (NAME, "m"),
            (OP, "."),
            (NAME, "hexdigest"),
            (OP, "("),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "return"),
            (NAME, "h"),
            (OP, "!="),
            (NAME, "ihash"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
        ]

    def add_evasion(self, tokens):
        """Detect if the source code has been tampered.

        Only works when executing from a file.
        """
        return [
            *self.import_tokens(),
            (NEWLINE, "\n"),
            (NAME, "if"),
            (LPAR, "("),
            (NAME, "integrity"),
            (OP, "("),
            (STRING, '"a"'),
            (OP, ")"),
            (RPAR, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "    "),
            *self.fail_call_tokens(),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            *tokens,
        ]

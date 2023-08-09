from tokenize import LPAR, NAME, NEWLINE, NUMBER, OP, RPAR, STRING


class TokensObfuscator:
    """Store tokens, and untokenize to exec at runtime."""

    def import_tokens(self):
        return [
            (NAME, "from"),
            (NAME, "tokenize"),
            (NAME, "import"),
            (NAME, "untokenize"),
        ]

    def generate_tokens_list(self, tokens):
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

    def obfuscate_tokens(self, tokens):
        return [
            *self.import_tokens(),
            (NEWLINE, "\n"),
            (NAME, "exec"),
            (LPAR, "("),
            (NAME, "untokenize"),
            (LPAR, "("),
            *self.generate_tokens_list(tokens),
            (RPAR, ")"),
            (RPAR, ")"),
            (NEWLINE, "\n"),
        ]

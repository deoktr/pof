from tokenize import LPAR, NAME, NEWLINE, NUMBER, OP, RPAR, STRING


class TokensObfuscator:
    """Store tokens, and untokenize to exec at runtime."""

    @staticmethod
    def import_tokens():
        return [
            (NAME, "from"),
            (NAME, "tokenize"),
            (NAME, "import"),
            (NAME, "untokenize"),
        ]

    @staticmethod
    def generate_tokens_list(tokens):
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

    @classmethod
    def obfuscate_tokens(cls, tokens):
        return [
            *cls.import_tokens(),
            (NEWLINE, "\n"),
            (NAME, "exec"),
            (LPAR, "("),
            (NAME, "untokenize"),
            (LPAR, "("),
            *cls.generate_tokens_list(tokens),
            (RPAR, ")"),
            (RPAR, ")"),
            (NEWLINE, "\n"),
        ]

# TODO (204): calculate frequency based on the number of lines to distribute
# the comment evenly across the code
import random
from tokenize import COMMENT, DEDENT, INDENT, NEWLINE


class AddCommentsObfuscator:
    """Add comments to the code.

    Either use the generator or the comments below.
    """

    TODO = (
        "TODO: This is garbage code",
        "TODO: Remove this part, useless now",
        "TODO: not that",
        "TODO: repare this part",
        "TODO: remove",
        "TODO: clean",
        "TODO: use graphC to expose interface",
    )

    FIXME = (
        "FIXME: This doesn't work",
        "FIXME: do it right",
        "fixme, not working",
        "fix why use this ? better to use ecog",
    )

    LINTER = (
        "nosec",
        "noqa",
        "noqa: E122",
        "noqa: F403",
    )

    OTHER = (
        "WHO THE FUCK ADDED THAT ?",
        "what is that ?",
        "why?...",
        "????????",
        "???",
        "what",
        "why?",
        "WTF",
        "who wrote this part ?",
        "please not like that",
    )

    TROLL = (
        "Hello :)",
        "I SEE YOU",
        "I know who you are",
        "Made with ChatGPT",
        "Copyright Microsoft",
        "Made in China",
        "Made with love <3",
    )

    def __init__(self, frequency=0.03, generator=None, *, remove_used=True) -> None:
        self.frequency = frequency
        self.generator = generator

        self.remove_used = remove_used

        self.types = [
            self.TODO,
            self.FIXME,
            self.LINTER,
            self.OTHER,
            self.TROLL,
        ]

    def get_comment(self):
        comment_list = random.choice(self.types)
        if len(comment_list) > 0:
            if self.generator:
                number = random.randint(1, 12)
                comment = " ".join([next(self.generator) for _ in range(number)])
            else:
                comment = random.choice(comment_list)
                # if self.remove_used:
                #     comment_list.remove(comment)
            return f"# {comment}"
        return None

    def obfuscate_tokens(self, tokens):
        result = []  # obfuscated tokens
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            if (
                toknum in [NEWLINE, INDENT, DEDENT]
                and (random.randint(0, 100) / 100) <= self.frequency
            ):
                c = self.get_comment()
                if c is not None:
                    new_tokens.extend([(COMMENT, c), (NEWLINE, "\n")])

            if new_tokens:
                result.extend(new_tokens)
        return result

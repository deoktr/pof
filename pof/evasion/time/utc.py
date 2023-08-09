from tokenize import NAME, OP, STRING

from pof.evasion.base import BaseEvasion


class UTCEvasion(BaseEvasion):
    def import_tokens(self):
        return [
            (NAME, "import"),
            (NAME, "time"),
        ]

    def check_tokens(self):
        """Validates system does not use UTC timezone.

        `"UTC" in time.tzname`
        """
        return [
            (STRING, '"UTC"'),
            (NAME, "in"),
            (NAME, "time"),
            (OP, "."),
            (NAME, "tzname"),
        ]

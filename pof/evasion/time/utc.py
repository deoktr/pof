from tokenize import NAME, OP, STRING

from pof.evasion.base import BaseEvasion


class UTCEvasion(BaseEvasion):
    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "time"),
        ]

    @staticmethod
    def check_tokens():
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

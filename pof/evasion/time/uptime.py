# TODO (deoktr): windows version: https://www.geeksforgeeks.org/getting-the-time-since-os-startup-using-python/
from tokenize import LPAR, NAME, NUMBER, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class LinuxUptimeEvasion(BaseEvasion):
    def __init__(self, uptime=12 * 60) -> None:
        # uptime is in seconds
        # default: 12 minutes
        self.uptime = uptime

    @staticmethod
    def import_tokens():
        return [
            (NAME, "from"),
            (NAME, "pathlib"),
            (NAME, "import"),
            (NAME, "Path"),
        ]

    def check_tokens(self):
        """Validates system does not use UTC timezone.

        `float(Path("/proc/uptime").read_text().split()[0]) < 12**60`
        """
        return [
            (NAME, "float"),
            (LPAR, "("),
            (NAME, "Path"),
            (LPAR, "("),
            (STRING, repr("/proc/uptime")),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "read_text"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "split"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "["),
            (NUMBER, "0"),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.uptime)),
        ]

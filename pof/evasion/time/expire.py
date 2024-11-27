from datetime import UTC, datetime, timedelta
from tokenize import LPAR, NAME, NUMBER, OP, RPAR

from pof.evasion.base import BaseEvasion


class ExpireEvasion(BaseEvasion):
    def __init__(self, under_datetime=None, over_datetime=None) -> None:
        """Expire after a certain time (default 15 minutes)."""
        if under_datetime is None:
            under_datetime = datetime.now(tz=UTC) + timedelta(minutes=15)
        self.under_datetime = under_datetime

        # TODO (deoktr): remove random timedelta to now, as to not give the date/time of
        # payload creation
        if over_datetime is None:
            over_datetime = datetime.now(tz=UTC)
        self.over_datetime = over_datetime

    @staticmethod
    def import_tokens():
        return [
            (NAME, "from"),
            (NAME, "datetime"),
            (NAME, "import"),
            (NAME, "datetime"),
        ]

    def check_tokens(self):
        """Time expiry check tokens.

        `datetime(2023,1,1,1,1)>datetime.utcnow()
            or datetime.utcnow()>datetime(2023,1,2,1,1,1)`
        """
        return [
            (NAME, "datetime"),
            (LPAR, "("),
            (NUMBER, str(self.over_datetime.year)),
            (OP, ","),
            (NUMBER, str(self.over_datetime.month)),
            (OP, ","),
            (NUMBER, str(self.over_datetime.day)),
            (OP, ","),
            (NUMBER, str(self.over_datetime.hour)),
            (OP, ","),
            (NUMBER, str(self.over_datetime.minute)),
            (RPAR, ")"),
            (OP, ">"),
            (NAME, "datetime"),
            (OP, "."),
            (NAME, "utcnow"),
            (LPAR, "("),
            (RPAR, ")"),
            (NAME, "or"),
            (NAME, "datetime"),
            (OP, "."),
            (NAME, "utcnow"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, ">"),
            (NAME, "datetime"),
            (LPAR, "("),
            (NUMBER, str(self.under_datetime.year)),
            (OP, ","),
            (NUMBER, str(self.under_datetime.month)),
            (OP, ","),
            (NUMBER, str(self.under_datetime.day)),
            (OP, ","),
            (NUMBER, str(self.under_datetime.hour)),
            (OP, ","),
            (NUMBER, str(self.under_datetime.minute)),
            (OP, ","),
            (NUMBER, str(self.under_datetime.second)),
            (RPAR, ")"),
        ]

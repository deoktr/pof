from tokenize import NEWLINE, OP

from pof.evasion.base import BaseEvasion

from .cpu.cpu_count import CPUCountEvasion
from .hooks.debugger import DebuggerEvasion
from .time.expire import ExpireEvasion
from .time.utc import UTCEvasion


class MultiEvasion(BaseEvasion):
    def __init__(self, list_evasion=None) -> None:
        if list_evasion is None:
            list_evasion = [
                CPUCountEvasion(),
                DebuggerEvasion(),
                ExpireEvasion(),
                UTCEvasion(),
            ]
        self.list_evasion = list_evasion

    def import_tokens(self):
        tokens = []
        for evasion in self.list_evasion:
            if len(tokens) > 0:
                tokens.append((NEWLINE, "\n"))
            tokens.extend(evasion.import_tokens())
        return tokens

    def check_tokens(self):
        tokens = []
        for evasion in self.list_evasion:
            if len(tokens) > 0:
                tokens.append((OP, "or"))
            tokens.extend(
                [
                    (OP, "("),
                    *evasion.check_tokens(),
                    (OP, ")"),
                ],
            )
        return tokens

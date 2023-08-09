# just prompt the user with a dialog box
# TODO (204): test
# TODO (204): make a version for linux somehow
# TODO (204): close prompt after a certain time
from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class PromptBase:
    def __init__(self, title=None, message=None) -> None:
        # TODO (204): generate randomly the message and title
        if title is None:
            title = "System Error 0x18463832"
        if message is None:
            message = "Your system encountered an error, please click OK to proceed"

        self.message = message
        self.title = title


class LinuxPromptEvasion(BaseEvasion, PromptBase):
    """Prompt the user.

    Tkinter is required to prompt user on unix systems, you'll need the `libtk?`
    library. Run either `apt-get install tk`, `pacman -S tk` or `dnf install tk`.
    """

    def check_tokens(self):
        """Evasion is triggered if the message box is not pressed.

        ``
        """
        return [
            # TODO (204): check file `p.py` in the same directory
        ]


class WinPromptEvasion(BaseEvasion, PromptBase):
    def import_tokens(self):
        return [
            (NAME, "import"),
            (NAME, "ctypes"),
        ]

    def check_tokens(self):
        """Evasion is triggered if the message box is not pressed.

        `ctypes.windll.user32.MessageBoxW(None, message, title)`
        """
        return [
            (NAME, "not"),
            (NAME, "ctypes"),
            (OP, "."),
            (NAME, "windll"),
            (OP, "."),
            (NAME, "user32"),
            (OP, "."),
            (NAME, "MessageBoxW"),
            (LPAR, "("),
            (NAME, "None"),
            (OP, ","),
            (STRING, repr(self.message)),
            (OP, ","),
            (STRING, repr(self.title)),
            (RPAR, ")"),
        ]

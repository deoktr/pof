import io
from tokenize import LPAR, NAME, OP, RPAR, generate_tokens

from pof.evasion.base import BaseEvasion


class FileListMissingEvasion(BaseEvasion):
    def __init__(self, file_list) -> None:
        self.file_list = file_list

    def import_tokens(self):
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self):
        """Trigger evasion if any file from the list is present on the system.

        `any([os.path.isfile(p) for p in ['/tmp/a', '/tmp/b', ...]])`
        """
        # TODO (204): change
        io_obj = io.StringIO(repr(self.file_list))
        file_list_tokens = list(generate_tokens(io_obj.readline))

        return [
            (NAME, "any"),
            (LPAR, "("),
            (OP, "["),
            (NAME, "os"),
            (OP, "."),
            (NAME, "path"),
            (OP, "."),
            (NAME, "isfile"),
            (LPAR, "("),
            (NAME, "p"),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "p"),
            (NAME, "in"),
            *file_list_tokens,
            (OP, "]"),
            (RPAR, ")"),
        ]

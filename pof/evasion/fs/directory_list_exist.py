import io
from tokenize import LPAR, NAME, OP, RPAR, generate_tokens

from pof.evasion.base import BaseEvasion


class DirectoryListExistEvasion(BaseEvasion):
    def __init__(self, directory_list) -> None:
        self.directory_list = directory_list

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self):
        """Trigger evasion if any directory from the list is absent on the system.

        `not all([os.path.isdir(p)for p in['/tmp/a','/tmp/b',...]])`
        """
        # TODO (204): change
        io_obj = io.StringIO(repr(self.directory_list))
        directory_list_tokens = list(generate_tokens(io_obj.readline))

        return [
            (NAME, "not"),
            (NAME, "all"),
            (LPAR, "("),
            (OP, "["),
            (NAME, "os"),
            (OP, "."),
            (NAME, "path"),
            (OP, "."),
            (NAME, "isdir"),
            (LPAR, "("),
            (NAME, "p"),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "p"),
            (NAME, "in"),
            *directory_list_tokens,
            (OP, "]"),
            (RPAR, ")"),
        ]

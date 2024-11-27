import io
from tokenize import LPAR, NAME, OP, RPAR, generate_tokens

from pof.evasion.base import BaseEvasion


class FileListExistEvasion(BaseEvasion):
    def __init__(self, file_list) -> None:
        self.file_list = file_list

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self):
        """Trigger evasion if any file from the list is absent on the system.

        `not all([os.path.isfile(p)for p in['/tmp/a','/tmp/b',...]])`
        """
        # TODO (deoktr): change
        io_obj = io.StringIO(repr(self.file_list))
        file_list_tokens = list(generate_tokens(io_obj.readline))

        return [
            (NAME, "not"),
            (NAME, "all"),
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

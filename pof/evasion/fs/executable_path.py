import io
from tokenize import LPAR, NAME, OP, RPAR, generate_tokens

from pof.evasion.base import BaseEvasion


class ExecPathEvasion(BaseEvasion):
    DEFAULT_CONTAIN_LIST = (
        "virus",
        "VIRUS",
        "sample",
        "SAMPLE",
        "sandbox",
        "SANDBOX",
        "malware",
        "Malware",
        # Anubis sandbox
        "InsideTm",
        "insidetm",
    )

    def __init__(self, contain_list=DEFAULT_CONTAIN_LIST) -> None:
        self.contain_list = contain_list

    def import_tokens(self):
        return [
            (NAME, "import"),
            (NAME, "pathlib"),
        ]

    def check_tokens(self):
        """Check if full exec path contains one of the specific strings.

        `any([s in str(pathlib.Path(__file__).absolute()) for s in["virus",...]])`
        """
        # TODO (204): generate tokens differently
        io_obj = io.StringIO(repr(self.contain_list))
        contain_list_tokens = list(generate_tokens(io_obj.readline))

        return [
            (NAME, "any"),
            (LPAR, "("),
            (OP, "["),
            (NAME, "s"),
            (NAME, "in"),
            (NAME, "str"),
            (LPAR, "("),
            (NAME, "pathlib"),
            (OP, "."),
            (NAME, "Path"),
            (LPAR, "("),
            (NAME, "__file__"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "absolute"),
            (LPAR, "("),
            (RPAR, ")"),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "s"),
            (NAME, "in"),
            *contain_list_tokens,
            (OP, "]"),
            (RPAR, ")"),
        ]

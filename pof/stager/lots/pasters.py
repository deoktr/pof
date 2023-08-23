from urllib import request

from pof.errors import PofError
from pof.stager import DownloadStager


class PasteRsStager(DownloadStager):
    """PasteRs.

    Code compatible with Python3 only (change in urllib names):

    Upload the code to paste.rs, and generate a stager to pull the code and
    execute it (using `exec`) from memory.

    No account is required to use paste.rs.
    """

    def upload(self, code):
        req = request.Request("https://paste.rs", data=code)

        r = request.urlopen(req)

        raw_link = r.read().decode()
        valid_code = 201
        if r.code != valid_code:
            msg = f"Failed to upload to paste.rs, got code {r.code}"
            raise PofError(msg)

        return raw_link

# POF, a free and open source Python obfuscation framework.
# Copyright (C) 2022 - 2025  POF Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# ruff: noqa: S310
import random
from urllib import request

from pof.errors import PofError
from pof.stager import DownloadStager


class Cl1pNetStager(DownloadStager):
    """Cl1p.net.

    Code compatible with Python3 only (change in urllib names):

    Upload the code to paste.rs, and generate a stager to pull the code and
    execute it (using `exec`) from memory.

    No account is required to use cl1p.net, but it's limited to 10 paste per days.
    """

    def __init__(
        self,
        api_token="EXAMPLE_TOKEN",  # noqa: S107
        *args,
        **kwargs,
    ) -> None:
        self.api_token = api_token
        super().__init__(*args, **kwargs)

    def upload(self, code, path=None):
        if path is None:
            random_path = "".join(
                [random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(13)],
            )
        url = "https://api.cl1p.net/" + random_path
        req = request.Request(
            url,
            data=code,
            headers={
                "cl1papitoken": self.api_token,
                "Content-Type": "text/html; charset=UTF-8",
            },
        )

        r = request.urlopen(req)

        success_code = 201
        if r.code != success_code:
            msg = f"Failed to upload to cl1p.net, got code {r.code}"
            raise PofError(msg)

        return url

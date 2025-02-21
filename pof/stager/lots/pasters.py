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

    @staticmethod
    def upload(code):
        req = request.Request("https://paste.rs", data=code)

        r = request.urlopen(req)  # noqa: S310

        raw_link = r.read().decode()
        valid_code = 201
        if r.code != valid_code:
            msg = f"Failed to upload to paste.rs, got code {r.code}"
            raise PofError(msg)

        return raw_link

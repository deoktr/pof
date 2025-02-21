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

from urllib import parse, request

from pof.stager import DownloadStager


class PastebinStager(DownloadStager):
    """Pastebin.

    Code compatible with Python3 only (change in urllib names):

    Upload the code to pastebin, and generate a stager to pull the code and
    execute it (using `exec`) from memory.

    You will need to create an account on pastebin and get your API key to be
    able to upload to it.
    """

    def __init__(self, api_dev_key, *args, **kwargs) -> None:
        self.api_dev_key = api_dev_key
        super().__init__(*args, **kwargs)

    def upload(self, code):
        dumps_params = {
            "api_dev_key": self.api_dev_key,
            "api_paste_code": code,
            "api_option": "paste",
        }
        post_data = parse.urlencode(dumps_params).encode()
        req = request.Request("https://pastebin.com/api/api_post.php", data=post_data)

        # TODO (deoktr): check return code
        r = request.urlopen(req)  # noqa: S310

        link = r.read().decode()
        return "https://pastebin.com/raw/" + link.split("/")[-1]

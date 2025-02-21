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

from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion


class TmpCountEvasion(BaseEvasion):
    """Cross-platform evasion that count the number of temp files."""

    def __init__(self, tmp_count=5) -> None:
        self.tmp_count = tmp_count

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
            (OP, ","),
            (NAME, "sys"),
        ]

    def check_tokens(self):
        r"""Check the number of files present in /tmp.

        `len(os.listdir("/tmp"if sys.platform!="windows"else"C:\windows\temp"))<10`
        """
        return [
            (NAME, "len"),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "listdir"),
            (LPAR, "("),
            (STRING, repr("/tmp")),  # noqa: S108
            (NAME, "if"),
            (NAME, "sys"),
            (OP, "."),
            (NAME, "platform"),
            (OP, "!="),
            (STRING, repr("windows")),
            (NAME, "else"),
            (STRING, repr("C:\\windows\\temp")),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "<"),
            (STRING, repr(self.tmp_count)),
        ]


class LinuxTmpCountEvasion(BaseEvasion):
    def __init__(self, tmp_count=5) -> None:
        self.tmp_count = tmp_count

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
            (OP, ","),
            (NAME, "sys"),
        ]

    def check_tokens(self):
        """Check the number of files present in /tmp.

        `len(os.listdir("/tmp")) < 10`
        """
        return [
            (NAME, "len"),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "listdir"),
            (LPAR, "("),
            (STRING, repr("/tmp")),  # noqa: S108
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "<"),
            (STRING, repr(self.tmp_count)),
        ]


class WinTmpCountEvasion(BaseEvasion):
    def __init__(self, tmp_count=5) -> None:
        self.tmp_count = tmp_count

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
            (OP, ","),
            (NAME, "sys"),
        ]

    def check_tokens(self):
        r"""Check the number of files present in /tmp.

        `len(os.listdir("C:\windows\temp")) < 10`
        """
        return [
            (NAME, "len"),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "listdir"),
            (LPAR, "("),
            (STRING, repr(r"C:\windows\temp")),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "<"),
            (STRING, repr(self.tmp_count)),
        ]

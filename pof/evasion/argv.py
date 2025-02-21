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

from tokenize import NAME, NUMBER, OP, STRING

from pof.evasion.base import BaseEvasion


class ArgvEvasion(BaseEvasion):
    """Ensure that the correct argument is passed."""

    def __init__(self, argv="argv", position=1) -> None:
        self.argv = argv
        # can put -1 in position to select the last argument
        self.position = position

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "sys"),
        ]

    def check_tokens(self):
        """Argument check tokens.

        `len(sys.argv)==1 or sys.argv[1]!="123"`
        """
        return [
            (NAME, "len"),
            (OP, "("),
            (NAME, "sys"),
            (OP, "."),
            (NAME, "argv"),
            (OP, ")"),
            (OP, "=="),
            (NUMBER, str(self.position)),
            (NAME, "or"),
            (NAME, "sys"),
            (OP, "."),
            (NAME, "argv"),
            (OP, "["),
            (NUMBER, str(self.position)),
            (OP, "]"),
            (OP, "!="),
            (STRING, repr(self.argv)),
        ]

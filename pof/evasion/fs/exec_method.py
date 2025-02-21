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

from tokenize import NAME, OP

from pof.evasion.base import BaseEvasion


class ExecMethodEvasion(BaseEvasion):
    def __init__(self, method="file") -> None:
        # "file" or "memory"
        self.exec_method = method

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "time"),
        ]

    def check_tokens(self):
        """Verify the execution method.

        When Python code is executed from the console or from the memory
        directly the `__file__` object will be equal to `<stdin>`, if a script
        is meant to be launched with a specific method the evasion can be added.

        Usage:

        This doesn't work (trigger evasion when file is selected)
        ```bash
        echo "print(__file__)" | ./pof.py ... | python
        Exception: evasion check triggered
        ```

        This works (doesn't trigger evasion when file is selected)
        ```bash
        echo "print(__file__)" | ./pof.py ... > bin/a.py & python bin/a.py
        /path/to/file/bin/a.py
        ```

        Todo:
        If running from the console `__file__` doesn't exist, this needs to be
        taken into account !
        """
        equal = "=!"
        if self.exec_method == "file":
            equal = "=="

        return [
            (NAME, "__file__"),
            (OP, equal),
            (NAME, repr("<stdin>")),
        ]

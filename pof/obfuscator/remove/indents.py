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

# TODO (deoktr): support multi symbols indents (mix spaces and tabs)
# this might be extremly difficult because we'll have to keep track of the
# current function/class declaration, we can't mix inside the same function be
# between multiple we can
from tokenize import DEDENT, INDENT


class IndentsObfuscator:
    """Remove indents to minimum."""

    def __init__(self, indent=" ") -> None:
        self.indent = indent

    def obfuscate_tokens(self, tokens):
        result = []  # obfuscated tokens
        depth = 0  # indent depth
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            if toknum == INDENT:
                depth += 1
                new_tokens = [(toknum, depth * self.indent)]
            elif toknum == DEDENT:
                depth -= 1

            if new_tokens:
                result.extend(new_tokens)
        return result

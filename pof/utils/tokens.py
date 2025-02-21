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

from itertools import chain
from tokenize import (
    DEDENT,
    ENCODING,
    INDENT,
    NAME,
    NEWLINE,
    NL,
    NUMBER,
    STRING,
    Untokenizer,
)


class NoSpaceUntokenizer(Untokenizer):
    """Custom Untokenizer that remove useless spaces after every NAME or NUMBER."""

    def compat(self, token, iterable):  # noqa: C901
        indents = []
        toks_append = self.tokens.append
        startline = token[0] in (NEWLINE, NL)
        prevstring = False
        prevname = False

        for tok in chain([token], iterable):
            toknum, tokval = tok[:2]
            if toknum == ENCODING:
                self.encoding = tokval
                continue

            # just a quick change to the way this part works so that spaces are
            # not added everywhere and everytimes just when it's needed
            if toknum in (NAME, NUMBER):
                if prevname:
                    tokval = " " + tokval
                prevname = True
            else:
                prevname = False

            # Insert a space between two consecutive strings
            if toknum == STRING:
                if prevstring or tokval[0] not in "'\"":
                    tokval = " " + tokval
                prevstring = True
            else:
                prevstring = False

            if toknum == INDENT:
                indents.append(tokval)
                continue
            if toknum == DEDENT:
                indents.pop()
                continue
            if toknum in (NEWLINE, NL):
                startline = True
            elif startline and indents:
                toks_append(indents[-1])
                startline = False
            toks_append(tokval)


def untokenize(iterable):
    """Custom untokenize definition to use the NoSpaceUntokenizer."""
    ut = NoSpaceUntokenizer()
    out = ut.untokenize(iterable)
    if ut.encoding is not None:
        out = out.encode(ut.encoding)
    return out

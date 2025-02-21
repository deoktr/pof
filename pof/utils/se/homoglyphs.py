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

"""Social engineering homoglyphs generators."""

import contextlib
import random
from pathlib import Path

from pof.errors import PofError


class HomoglyphsGenerator:
    """Homoglyphs (look-alike) generator.

    https://en.wikipedia.org/wiki/Homoglyph
    """

    # TODO (deoktr): add ability to specify the homoglyphs file
    # TODO (deoktr): cache this function
    @classmethod
    def get_homoglyphs_dict(cls):
        homoglyphs = {}
        file = Path(__file__).parent / "homoglyphs.txt"
        with file.open() as file:
            for fullline in file:
                line = fullline[:-1]
                if line.startswith("#"):
                    continue
                homoglyphs.update({line[0]: line[1:]})
        return homoglyphs

    @classmethod
    def get_homoglyphs_char_list(cls, char: str) -> list[str]:
        homoglyphs = cls.get_homoglyphs_dict()
        if char in homoglyphs:
            return homoglyphs[char]
        return [char]

    @classmethod
    def get_homoglyphs_char(cls, char: str) -> str:
        homoglyphs = cls.get_homoglyphs_char_list(char)
        if len(homoglyphs) == 0 or (len(homoglyphs) == 1 and homoglyphs[0] == char):
            msg = "no homoglyphs available for this character"
            raise PofError(msg)
        return random.choice(homoglyphs)

    @classmethod
    def get_full_homoglyphs(cls, string: str) -> str:
        """Get a full homoglyphs.

        Return a string composed entirely of homoglyphs.
        """
        new_string = ""
        for char in string:
            try:
                homoglyph = cls.get_homoglyphs_char(char)
            except PofError:
                homoglyph = char
            new_string += homoglyph
        return new_string

    @classmethod
    def get_single_homoglyph(cls, string: str, max_fails: int = 20) -> str:
        """Get a partial homoglyphs on a single random character."""
        homoglyph = None
        fails = 0
        while homoglyph is None:
            index = random.randint(0, len(string) - 1)
            try:
                homoglyph = cls.get_homoglyphs_char(string[index])
            except Exception as err:
                fails += 1
                if fails > max_fails:
                    msg = "failed to find homoglyph"
                    raise PofError(msg) from err
                continue
            else:
                break
        return string[:index] + homoglyph + string[index + 1 :]

    @classmethod
    def get_homoglyphs(cls, string: str, freq: float = 0.2) -> str:
        """Get a partial homoglyphs.

        Return a string composed of some homoglyphs.
        """
        new_string = ""
        for char in string:
            homo = random.randint(0, 100)
            new_char = char
            if homo / 100 < freq:
                with contextlib.suppress(Exception):
                    new_char = cls.get_homoglyphs_char(char)
            new_string += new_char

        # Ensure at least one char is changed !
        # yes this is not the cleanest way, but it works for now
        if new_string == string:
            return cls.get_single_homoglyph(string)

        return new_string

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

"""Unicode random names generators."""

import ast
import random

from .base import BaseGenerator
from pof.logger import logger


class UnicodeGenerator(BaseGenerator):
    @classmethod
    def _unicode_generator(cls, unicode_list, min_length: int = 1, max_length: int = 5):
        previous = []
        while True:
            # TODO (deoktr): add code to increase max_length if can't create new names
            length = random.randint(min_length, max_length)
            name = ""
            for _ in range(length):
                name += random.choice(unicode_list)
            if name in previous or name in cls.RESERVED:
                continue
            try:
                ast.parse(f"{name}=None")

                # if we need to call `getattr` on the variable name, then normalize
                # the variable name BEFORE adding it to the string, or uncomment the
                # following to
                #
                # https://github.com/python/cpython/issues/104458
                # https://docs.python.org/3/reference/lexical_analysis.html#identifiers
                # code = f"class a:\n {name}=None\ngetattr(a, {repr(name)})"
                # try:
                #     exec(code)
                # except AttributeError:
                #     continue

            except Exception:  # noqa: BLE001
                logger.debug("Unicode %s doesn't work", name)
                continue
            previous.append(name)
            yield name

    @classmethod
    def broken_generator(cls):
        # collection of cursed unicode ranges
        broken_range = [
            # https://en.wikipedia.org/wiki/Cuneiform_(Unicode_block)
            *map(chr, range(0x12000, 0x123FF)),
            # https://en.wikipedia.org/wiki/Cuneiform_Numbers_and_Punctuation
            *map(chr, range(0x12400, 0x12474)),
            # https://en.wikipedia.org/wiki/Early_Dynastic_Cuneiform_(Unicode_block)
            *map(chr, range(0x12480, 0x12543)),
        ]
        return cls._unicode_generator(broken_range, max_length=1)

    @classmethod
    def weird_generator(cls):
        weird_range = [
            *map(chr, range(0x01C0, 0x01C3)),  # African clicks
            *map(chr, range(0x01F1, 0x01F3)),
            chr(0x01F6),
            chr(0x01FC),
            chr(0x01FD),
            *map(chr, range(0x02A3, 0x02AD)),
            # small symbols dots
            *map(chr, range(0x02B0, 0x036F)),
            # https://en.wikipedia.org/wiki/Anatolian_Hieroglyphs_(Unicode_block)
            *map(chr, range(0x14400, 0x1467F)),
            # https://en.wikipedia.org/wiki/Ancient_Greek_Numbers_(Unicode_block)
            *map(chr, range(0x10140, 0x1018F)),
            # https://en.wikipedia.org/wiki/Glagolitic_(Unicode_block)
            *map(chr, range(0x2C00, 0x2C5F)),
            # https://en.wikipedia.org/wiki/Meroitic_Hieroglyphs_(Unicode_block)
            *map(chr, range(0x10980, 0x1099F)),
            # https://en.wikipedia.org/wiki/Runic_(Unicode_block)
            *map(chr, range(0x16A0, 0x16FF)),
        ]
        return cls._unicode_generator(weird_range, max_length=3)

    @classmethod
    def ideograms_generator(cls):
        ideograms_range = [
            # https://en.wikipedia.org/wiki/Linear_A_(Unicode_block)
            # *map(chr, range(0x10600, 0x1077F)),
            # https://en.wikipedia.org/wiki/Linear_B_Ideograms
            *map(chr, range(0x10080, 0x100FF)),
        ]
        return cls._unicode_generator(ideograms_range, max_length=2)

    @classmethod
    def dot_generator(cls):
        return cls._unicode_generator(list(map(chr, range(0x02B0, 0x036F))))

    @classmethod
    def canadian_aboriginal_generator(cls):
        # https://en.wikipedia.org/wiki/Unified_Canadian_Aboriginal_Syllabics_(Unicode_block)
        return cls._unicode_generator(list(map(chr, range(0x1400, 0x167F))))

    @classmethod
    def runic_generator(cls):
        # https://en.wikipedia.org/wiki/Runic_(Unicode_block)
        return cls._unicode_generator(
            list(map(chr, range(0x16A0, 0x16FF))),
            max_length=8,
        )

    @classmethod
    def katakana_generator(cls):
        # https://en.wikipedia.org/wiki/Katakana_(Unicode_block)
        return cls._unicode_generator(list(map(chr, range(0x30A0, 0x30FF))))

    @classmethod
    def cjk_generator(cls):
        # https://en.wikipedia.org/wiki/CJK_Unified_Ideographs
        return cls._unicode_generator(
            list(map(chr, range(0x4E00, 0x9FFF))),
            max_length=3,
        )

    @classmethod
    def egyptian_hieroglyphs_generator(cls):
        # https://en.wikipedia.org/wiki/Egyptian_Hieroglyphs_(Unicode_block)
        return cls._unicode_generator(list(map(chr, range(0x13000, 0x1342E))))

    @classmethod
    def arabic_generator(cls):
        # https://en.wikipedia.org/wiki/Arabic_script_in_Unicode
        arabic_range = [
            *map(chr, range(0x0600, 0x06FF)),
            *map(chr, range(0x1EE00, 0x1EEFF)),
        ]
        return cls._unicode_generator(arabic_range, max_length=8)

    @classmethod
    def latin_generator(cls):
        latin_range = [
            *map(chr, range(0x0041, 0x005A)),
            *map(chr, range(0x0061, 0x007A)),
            *map(chr, range(0x00C0, 0x01BF)),
            *map(chr, range(0x1E00, 0x1EFF)),
        ]
        return cls._unicode_generator(latin_range)

    @classmethod
    def cyrillic_generator(cls, supplement=False):  # noqa: FBT002
        # https://en.wikipedia.org/wiki/Cyrillic_script_in_Unicode
        cyrillic_range = list(map(chr, range(0x0400, 0x04FF)))
        if supplement:
            cyrillic_range.extend(
                [
                    *map(chr, range(0x0500, 0x052F)),
                    *map(chr, range(0x2DE0, 0x2DFF)),
                    *map(chr, range(0xA640, 0xA69F)),
                    *map(chr, range(0x1C80, 0x1C8F)),
                    *map(chr, range(0x1E030, 0x1E08F)),
                ],
            )
        return cls._unicode_generator(cyrillic_range)

    @classmethod
    def greek_generator(cls, supplement=False):  # noqa: FBT002
        # https://en.wikipedia.org/wiki/Greek_script_in_Unicode
        greek_range = list(map(chr, range(0x0370, 0x03FF)))
        if supplement:
            greek_range.extend(
                [
                    *map(chr, range(0x1D00, 0x1D7F)),
                    *map(chr, range(0x1F00, 0x1FFF)),
                    *map(chr, range(0x10140, 0x1018F)),
                ],
            )
        return cls._unicode_generator(greek_range)

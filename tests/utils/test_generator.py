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

import ast

from pof.utils.generator import AdvancedGenerator, BasicGenerator, UnicodeGenerator

r = 100


def test_basic_generator():
    generators = [
        BasicGenerator.alphabet_generator(),
        BasicGenerator.number_name_generator(),
        BasicGenerator.single_symbol_generator(),
        BasicGenerator.pointer_generator(),
        BasicGenerator.function_generator(),
        BasicGenerator.class_generator(),
    ]

    for generator in generators:
        names = []
        for _ in range(r):
            new = next(generator)
            assert new not in names
            assert ast.parse(f"{new} = 0")
            names.append(new)


def test_advanced_generator():
    generators = [
        AdvancedGenerator.realistic_generator(),
        AdvancedGenerator.fixed_length_generator(),
        AdvancedGenerator.multi_generator(
            {
                1: BasicGenerator.alphabet_generator(),
                5: BasicGenerator.number_name_generator(),
            }
        ),
    ]

    for generator in generators:
        names = []
        for _ in range(r):
            new = next(generator)
            assert new not in names
            assert ast.parse(f"{new} = 0")
            names.append(new)


def test_unicode_generator():
    generators = [
        UnicodeGenerator.broken_generator(),
        UnicodeGenerator.ideograms_generator(),
        UnicodeGenerator.weird_generator(),
        UnicodeGenerator.ideograms_generator(),
        UnicodeGenerator.dot_generator(),
        UnicodeGenerator.canadian_aboriginal_generator(),
        UnicodeGenerator.runic_generator(),
        UnicodeGenerator.katakana_generator(),
        UnicodeGenerator.cjk_generator(),
        UnicodeGenerator.egyptian_hieroglyphs_generator(),
        UnicodeGenerator.arabic_generator(),
        UnicodeGenerator.latin_generator(),
        UnicodeGenerator.cyrillic_generator(),
        UnicodeGenerator.greek_generator(),
    ]

    for generator in generators:
        names = []
        for _ in range(r):
            new = next(generator)
            assert new not in names
            assert ast.parse(f"{new} = 0")
            names.append(new)

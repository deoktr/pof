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

from pof.utils.generator import AdvancedGenerator, BasicGenerator

r = 100


def test_number_name_generator():
    generator = BasicGenerator.number_name_generator()
    names = []
    for _ in range(r):
        new = next(generator)
        assert new not in names
        names.append(new)


def test_alphabet_generator():
    generator = BasicGenerator.alphabet_generator()
    names = []
    for _ in range(r):
        new = next(generator)
        assert new not in names
        names.append(new)


def test_realistic_generator():
    generator = AdvancedGenerator.realistic_generator()
    names = []
    for _ in range(r):
        new = next(generator)
        assert new not in names
        names.append(new)


def test_multi_generator():
    gen_dict = {
        1: BasicGenerator.alphabet_generator(),
        5: BasicGenerator.number_name_generator(),
    }
    generator = AdvancedGenerator.multi_generator(gen_dict)
    names = []
    for _ in range(r):
        new = next(generator)
        assert new not in names
        names.append(new)

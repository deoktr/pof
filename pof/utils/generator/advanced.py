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

"""Advanced random names generators."""

import random
from pathlib import Path

from .base import BaseGenerator
from .basic import BasicGenerator


class AdvancedGenerator(BaseGenerator):
    @classmethod
    def realistic_generator(cls):
        file = Path(__file__).parent / "names.txt"
        with file.open() as file:
            name_list = [line.rstrip() for line in file]
        previous = []
        while True:
            name = random.choice(name_list)
            if name in previous or name in cls.RESERVED:
                continue
            previous.append(name)
            yield name

    @classmethod
    def fixed_length_generator(cls, chars="O0", first_chars="O", length=17):
        # inspired by: https://pyob.oxyry.com/
        gen = BasicGenerator.alphabet_generator(
            chars=chars,
            first_chars=first_chars,
            min_length=length,
            max_length=length,
        )
        while True:
            yield next(gen)

    @classmethod
    def multi_generator(cls, gen_dict):
        """Combine multiple generator.

        Take a dict of generator, with the key being the probability of it being
        used, must be an int.
        """
        list_generators = []
        for key, value in gen_dict.items():
            list_generators.extend(key * [value])
        previous = []
        while True:
            generator = random.choice(list_generators)
            name = next(generator)
            if name in previous or name in cls.RESERVED:
                continue
            previous.append(name)
            yield name

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

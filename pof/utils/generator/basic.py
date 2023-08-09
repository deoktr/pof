"""Basic random names generators."""
import random

from .base import BaseGenerator


class BasicGenerator(BaseGenerator):
    @classmethod
    def alphabet_generator(
        cls,
        min_length: int = 3,
        max_length: int = 10,
        chars: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_____",
        first_chars: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    ):
        """Random words that can be variables."""
        previous = []
        if first_chars is None:
            first_chars = chars
        while True:
            if min_length != max_length:
                length = random.randint(min_length, max_length)
            else:
                length = max_length
            name = random.choice(first_chars)
            for _ in range(length - 1):
                name += random.choice(chars)
            if name in previous or name in cls.RESERVED:
                continue
            previous.append(name)
            yield name

    @classmethod
    def number_name_generator(cls, length=1, prefix="_"):
        """Generator for endless number of variable name."""
        numbers = list(range(10**length, 10 ** (length + 1)))
        while True:
            if len(numbers) == 0:
                length += 1
                numbers = list(range(10**length, 10 ** (length + 1)))
            n = random.choice(numbers)
            numbers.remove(n)
            yield prefix + str(n)

    @classmethod
    def single_symbol_generator(cls, symbol="_"):
        # TODO (204): generate a couple in a list, randomize the order and take them
        # instead of increasing it by one in order
        length = 1
        while True:
            length += 1
            yield symbol * length

    @classmethod
    def pointer_generator(
        cls,
        name_format="_0x{}",
        length=12,
        chars="0123456789abcdef",
    ):
        """Generate var names in the format of hexadecimal."""
        ag = cls.alphabet_generator(
            min_length=length,
            max_length=length,
            chars=chars,
            first_chars=chars,
        )
        while True:
            name = next(ag)
            yield name_format.format(name)

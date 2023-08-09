"""Social engineering homoglyphs generators."""
import pathlib
import random


class HomoglyphsGenerator:
    """Homoglyphs (look-alike) generator.

    https://en.wikipedia.org/wiki/Homoglyph
    """

    # TODO (2O4): add ability to specify the homoglyphs file
    # TODO (2O4): cache this function
    @classmethod
    def get_homoglyphs_dict(cls):
        homoglyphs = {}
        file = pathlib.Path(__file__).parent / "homoglyphs.txt"
        with file.open() as file:
            for fullline in file:
                line = fullline[:-1]
                if line.startswith("#"):
                    continue
                homoglyphs.update({line[0]: line[1:]})
        return homoglyphs

    @classmethod
    def get_homoglyphs_char(cls, char: str):
        homoglyphs = cls.get_homoglyphs_dict()
        if char in homoglyphs:
            return homoglyphs[char]
        return [char]

    @classmethod
    def get_full_homoglyphs(cls, string: str) -> str:
        """Get a full homoglyphs.

        Return a string composed entirely of homoglyphs.
        """
        new_string = ""
        for char in string:
            homoglyphs = cls.get_homoglyphs_char(char)
            new_char = random.choice(homoglyphs)
            new_string += new_char
        return new_string

    # TODO (2O4): ensure that at least one character is changed !
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
                homoglyphs = cls.get_homoglyphs_char(char)
                new_char = random.choice(homoglyphs)
            new_string += new_char
        return new_string

from pof.utils.se import HomoglyphsGenerator

r = 100

chars = "abcdefghjklmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ0123456789"

special = [
    "!",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    "-",
    ".",
    "/",
    ":",
    ";",
    "<",
    "=",
    ">",
    "?",
    "@",
    "\\",
    "^",
    "_",
    "{",
    "}",
    "~",
    "¯",
]


def test_homoglyphs_char_generator():
    generator = HomoglyphsGenerator()
    for c in chars:
        h = generator.get_homoglyphs_char(c)
        assert c != h


def test_homoglyphs_special_char_generator():
    generator = HomoglyphsGenerator()
    for c in special:
        h = generator.get_homoglyphs_char(c)
        assert c != h


def test_get_single_homoglyph():
    generator = HomoglyphsGenerator()
    text = "Hello, world!"
    for _ in range(r):
        homo = generator.get_single_homoglyph(text)
        assert homo != text


def test_get_homoglyphs():
    generator = HomoglyphsGenerator()
    text = "Hello, world!"
    for _ in range(r):
        homo = generator.get_homoglyphs(text)
        assert homo != text

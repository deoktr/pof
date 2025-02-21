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

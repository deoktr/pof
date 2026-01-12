# POF, a free and open source Python obfuscation framework.
# Copyright (C) 2022 - 2026  Deoktr
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

import io

# to fix a problem "undefined b64decode" during exec
from base64 import b64decode  # noqa

from tokenize import generate_tokens, untokenize

from pof.obfuscator import XORObfuscator
from .utils import exec_capture

source = """
def main_function():
    x = "Hello"
    y = ", world!"
    print(x + y)

main_function()
"""


def test_XORObfuscator():
    io_obj = io.StringIO(source)
    tokens = list(generate_tokens(io_obj.readline))
    tokens = XORObfuscator().obfuscate_tokens(tokens)

    out = untokenize(tokens)
    captured_output = exec_capture(out, {"b64decode": b64decode})
    assert captured_output == "Hello, world!\n"

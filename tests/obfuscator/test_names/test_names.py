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

import io
import os
from tokenize import generate_tokens, untokenize

from pof.obfuscator import NamesObfuscator


# FIXME (deoktr): mock the generator function inside NamesObfuscator
# to produce var_name__, because if we put generator "O" then it will break with
def test_NamesObfuscator():
    def generator():
        while True:
            yield "O"

    source_file_path = os.path.join(os.path.dirname(__file__), "code", "source.py")
    with open(source_file_path) as f:
        source = f.read()

    io_obj = io.StringIO(source)
    tokens = list(generate_tokens(io_obj.readline))

    tokens = NamesObfuscator(generator=generator()).obfuscate_tokens(tokens)

    out = untokenize(tokens) + "\n"

    out_file_path = os.path.join(os.path.dirname(__file__), "code", "out.py")
    with open(out_file_path) as f:
        out_wanted = f.read()

    assert out == out_wanted

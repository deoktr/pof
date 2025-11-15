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
from tokenize import generate_tokens, untokenize

from pof.obfuscator import PrintObfuscator
from .utils import exec_capture

source = """
import foo
from bar import koo
a=1
print("Hello, world!")
print(a)
a+=1
print(f"{a}")
print("aa", "oo")
print(foo())
print(foo("ho", koo(), "j", 42), "e")
if __name__ == "__main__":
    koo(a)
"""

result = '\nimport foo \nfrom bar import koo \na =1 \n\n\na +=1 \n\n\n\n\nif __name__ =="__main__":\n    koo (a )\n'


def test_PrintObfuscator():
    io_obj = io.StringIO(source)
    tokens = list(generate_tokens(io_obj.readline))
    tokens = PrintObfuscator().obfuscate_tokens(tokens)

    for _index, (_toknum, tokval, *_) in enumerate(tokens):
        assert tokval != "print"

    out = untokenize(tokens)
    assert out == result

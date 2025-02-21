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

from pof.obfuscator import ExceptionObfuscator

source = """
import foo
from bar import koo
a=1
raise Exception("Hello, world!")
raise Exception(a)
a+=1
raise Exception(f"{a}")
raise OSError("aa", "oo")
raise CustomError(foo())
raise Exception(foo("ho", koo(), "j", 42), "e")
if __name__ == "__main__":
    koo(a)
"""


def test_PrintObfuscator_add_codes_false():
    io_obj = io.StringIO(source)
    tokens = list(generate_tokens(io_obj.readline))
    tokens = ExceptionObfuscator().obfuscate_tokens(tokens)

    result = '\nimport foo \nfrom bar import koo \na =1 \nraise Exception ()\nraise Exception ()\na +=1 \nraise Exception ()\nraise OSError ()\nraise CustomError ()\nraise Exception ()\nif __name__ =="__main__":\n    koo (a )\n'

    out = untokenize(tokens)
    assert out == result


def test_PrintObfuscator_add_codes_true():
    def generator():
        while True:
            yield "_"

    io_obj = io.StringIO(source)
    tokens = list(generate_tokens(io_obj.readline))
    tokens = ExceptionObfuscator(
        add_codes=True,
        generator=generator(),
    ).obfuscate_tokens(tokens)

    result = '\nimport foo \nfrom bar import koo \na =1 \nraise Exception ("_")\nraise Exception ("_")\na +=1 \nraise Exception ("_")\nraise OSError ("_")\nraise CustomError ("_")\nraise Exception ("_")\nif __name__ =="__main__":\n    koo (a )\n'

    out = untokenize(tokens)
    assert out == result

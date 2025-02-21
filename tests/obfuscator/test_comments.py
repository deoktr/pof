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
from tokenize import COMMENT, generate_tokens, untokenize

from pof.obfuscator import CommentsObfuscator

source = """
'''multiline
docstring
'''

# ho
'''comment'''
import foo  # end of line comment
a=1
# comment
a+=1
class Foo:
    \"\"\"
    docstring
    \"\"\"
    m = 's'
    print("test")
    x = \"\"\"
    multiline string
    \"\"\"
if __name__ == "__main__":
    koo(a)
"""

result = '\n\n\n\n\nimport foo \na =1 \n\na +=1 \nclass Foo :\n\n    m =\'s\'\n    print ("test")\n    x ="""\n    multiline string\n    """\nif __name__ =="__main__":\n    koo (a )\n'


def test_CommentsObfuscator():
    io_obj = io.StringIO(source)
    tokens = list(generate_tokens(io_obj.readline))
    tokens = CommentsObfuscator().obfuscate_tokens(tokens)

    for _index, (toknum, _tokval, *_) in enumerate(tokens):
        assert toknum != COMMENT

    out = untokenize(tokens)
    assert out == result

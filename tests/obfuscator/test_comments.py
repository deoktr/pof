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

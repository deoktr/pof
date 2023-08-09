# FIXME
# currently when updating variable if the size of the name changes then
# everything breaks
import io
import logging
import random
import string
from tokenize import NAME, NEWLINE, NL, generate_tokens

from rope.base.project import Project
from rope.refactor.rename import Rename

logging.basicConfig(level=logging.DEBUG)


RESERVED_WORDS = [
    "print",
    "for",
    "in",
    "range",
    "while",
    "True",
    "import",
]

PADDING = 0


def rename(index, name, new_name):
    return Rename(project, file, index).get_changes(new_name)


def _get_tokens(code):
    io_obj = io.StringIO(code)
    return list(generate_tokens(io_obj.readline))


def find_var_pos(tokens, var):
    current_len = 1
    for toknum, tokval, start, end, _line in tokens:
        if toknum in [NEWLINE, NL]:
            current_len += end[1]
        if toknum == NAME and tokval not in RESERVED_WORDS and tokval == var:
            return current_len + start[1]
    return None


def list_vars(tokens):
    var_list = []
    for toknum, tokval, _start, _end, _line in tokens:
        if toknum == NAME and tokval not in var_list and tokval not in RESERVED_WORDS:
            var_list.append(tokval)
    return var_list


def find_vars_pos(tokens):
    previous = []
    current_len = 1
    for toknum, tokval, start, end, _line in tokens:
        if toknum in [NEWLINE, NL]:
            current_len += end[1]
        if toknum == NAME and tokval not in previous and tokval not in RESERVED_WORDS:
            previous.append(tokval)
            yield current_len + start[1], tokval


if __name__ == "__main__":
    with open("a.py") as f:
        code = f.read()
    tokens = _get_tokens(code)

    project = Project(".")
    file = project.get_resource("a.py")

    # find_var_pos should be a generator
    # for index, name in find_var_pos(tokens):

    # this is extyremly bad, open and closes the file to get the position of the
    # next token after being updated by rope, this is the best way I found so
    # far, because other seam too hard
    for name in list_vars(tokens):
        with open("a.py") as f:
            tokens = _get_tokens(f.read())
        new_name = "".join(
            [
                random.choice(string.ascii_lowercase)
                for x in range(random.randint(2, 5))
            ],
        )
        logging.debug(f"changing var {name} to {new_name}")
        index = find_var_pos(tokens, name)
        changes = rename(index, name, new_name)
        project.do(changes)
    project.close()

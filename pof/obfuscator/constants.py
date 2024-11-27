"""Extract constants and put them at the top of the script.

Can extract:

- string
- number (int, float...)
- builtins (str, exec, hex...)
"""

#
# Add variables for certain values
# ex:
#   if type(x) is int: ...
#
#   u = type
#   a = int
#   if u(x) is a: ...
#
# TODO (deoktr): add variables under imports as an option
# TODO (deoktr): add variables inside functions
# TODO (deoktr): add exclusions for strings and numbers
#

import random
from tokenize import DEDENT, ENCODING, INDENT, NAME, NEWLINE, NUMBER, OP, STRING


class ConstantsObfuscator:
    """Extract variables and put them at the top of the file.

    This will thus set strings, numbers etc. has constants.
    """

    # list(__builtins__.__dict__.keys())
    BUILTINS = (
        # look like it works now ?
        "__name__",  # doesn't work with 'if _name_ == "_main_": ...'
        "__doc__",
        "__package__",
        "__loader__",
        "__spec__",
        "__build_class__",
        "__import__",
        "abs",
        "all",
        "any",
        "ascii",
        "bin",
        "breakpoint",
        "callable",
        "chr",
        "compile",
        "delattr",
        "dir",
        "divmod",
        "eval",
        "exec",
        # used not to work but now it does I guess
        "format",  # try to change "{}".format('foo')
        "getattr",
        "globals",
        "hasattr",
        "hash",
        "hex",
        "id",
        "input",
        "isinstance",
        "issubclass",
        "iter",
        "aiter",
        "len",
        "locals",
        "max",
        "min",
        "next",
        "anext",
        "oct",
        "ord",
        "pow",
        "print",
        "repr",
        "round",
        "setattr",
        "sorted",
        "sum",
        "vars",
        "None",
        "Ellipsis",
        "NotImplemented",
        "False",
        "True",
        "bool",
        "memoryview",
        "bytearray",
        "bytes",
        "classmethod",
        "complex",
        "dict",
        "enumerate",
        "filter",
        "float",
        "frozenset",
        "property",
        "int",
        "list",
        "map",
        "object",
        "range",
        "reversed",
        "set",
        "slice",
        "staticmethod",
        "str",
        # "super",  # plain doesn't work
        "tuple",
        "type",
        "zip",
        "__debug__",
        "BaseException",
        "Exception",
        "TypeError",
        "StopAsyncIteration",
        "StopIteration",
        "GeneratorExit",
        "SystemExit",
        "KeyboardInterrupt",
        "ImportError",
        "ModuleNotFoundError",
        "OSError",
        "EnvironmentError",
        "IOError",
        "EOFError",
        "RuntimeError",
        "RecursionError",
        "NotImplementedError",
        "NameError",
        "UnboundLocalError",
        "AttributeError",
        "SyntaxError",
        "IndentationError",
        "TabError",
        "LookupError",
        "IndexError",
        "KeyError",
        "ValueError",
        "UnicodeError",
        "UnicodeEncodeError",
        "UnicodeDecodeError",
        "UnicodeTranslateError",
        "AssertionError",
        "ArithmeticError",
        "FloatingPointError",
        "OverflowError",
        "ZeroDivisionError",
        "SystemError",
        "ReferenceError",
        "MemoryError",
        "BufferError",
        "Warning",
        "UserWarning",
        "EncodingWarning",
        "DeprecationWarning",
        "PendingDeprecationWarning",
        "SyntaxWarning",
        "RuntimeWarning",
        "FutureWarning",
        "ImportWarning",
        "UnicodeWarning",
        "BytesWarning",
        "ResourceWarning",
        "ConnectionError",
        "BlockingIOError",
        "BrokenPipeError",
        "ChildProcessError",
        "ConnectionAbortedError",
        "ConnectionRefusedError",
        "ConnectionResetError",
        "FileExistsError",
        "FileNotFoundError",
        "IsADirectoryError",
        "NotADirectoryError",
        "InterruptedError",
        "PermissionError",
        "ProcessLookupError",
        "TimeoutError",
        "open",
        "quit",
        "exit",
        "copyright",
        "credits",
        "license",
        "help",
    )

    def __init__(
        self,
        generator=None,
        obf_builtins_rate=1,
        obf_string_rate=1,
        obf_number_rate=1,
    ) -> None:
        if generator is None:
            from pof.utils.generator import BasicGenerator

            generator = BasicGenerator.alphabet_generator()

        self.generator = generator

        self.obf_number_rate = obf_number_rate
        self.obf_builtins_rate = obf_builtins_rate
        self.obf_string_rate = obf_string_rate

    def obfuscate_variable(self, toknum, tokval, variables):
        if tokval not in variables:
            var_name = next(self.generator)
            variables.update({tokval: [var_name, toknum]})
        return [(NAME, variables[tokval][0])], variables

    def obfuscate_tokens(self, tokens):
        variables = {}
        result = []
        parenthesis_depth = 0  # parenthesis depth
        prev_tokval = None
        prev_toknum = None
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            next_toknum = None
            if len(tokens) > index + 1:
                next_toknum, next_tokval, *__ = tokens[index + 1]

            # context
            if toknum == OP and tokval == "(":
                parenthesis_depth += 1
            elif toknum == OP and tokval == ")":
                parenthesis_depth -= 1

            # obfuscation
            if (
                (
                    toknum == NAME
                    and tokval in self.BUILTINS
                    and prev_tokval != "."  # avoid changing class/imports functions
                    and (
                        parenthesis_depth == 0
                        or (parenthesis_depth > 0 and next_tokval != "=")
                    )
                    and (random.randint(0, 100) / 100) <= self.obf_builtins_rate
                )
                or (
                    # don't obfuscate docstrings
                    toknum == STRING
                    and prev_toknum
                    not in [
                        NEWLINE,
                        DEDENT,
                        INDENT,
                        ENCODING,
                    ]
                    and (random.randint(0, 100) / 100) <= self.obf_string_rate
                )
                or (
                    toknum == NUMBER
                    and (random.randint(0, 100) / 100) <= self.obf_number_rate
                )
            ):
                new_tokens, variables = self.obfuscate_variable(
                    toknum,
                    tokval,
                    variables,
                )

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval
            prev_toknum = toknum

        # randomize order
        variables = list(variables.items())
        random.shuffle(variables)
        variables = dict(variables)

        var_tokens = []
        for tokval, (var_name, toknum) in variables.items():
            var_tokens.extend(
                [
                    (NAME, var_name),
                    (OP, "="),
                    (toknum, tokval),
                    (NEWLINE, "\n"),
                ],
            )

        return var_tokens + result

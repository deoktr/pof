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

# TODO (deoktr): WORK IN PROGRESS !
#
# Look at `Ruff` for "variable extraction"
#
# IDEA: maybe put every declaration at the start of the function, so that it has way
#   less chance to break the actual function
#
# example output:
#
# ```
# import os
# BASE = "/home/test/"
# path = os.path.join(BASE, "file.txt")
# print(path)
# ```
#
# ```
# import os
# u = "/home/test/"
# BASE = u
# a = "file.txt"
# path = os.path.join(BASE, a)
# x = path
# print(x)
# ```
#
# FIXME (deoktr): parenthesis variables:
# ```
# if (
#    x < 1 and y > 2
# )
# ```
# this would break because the variables would be added INSIDE the parenthesis
#
#
# FIXME (deoktr): decorators:
# ```
# class Foo:
#     @classmethod
#     def bar(a=1, b=2):
#        pass
# ```
# after classmethod and before def variables a and b will be obfuscated,
# breaking the code
#
import keyword
from tokenize import DEDENT, ENCODING, INDENT, NAME, NEWLINE, NL, NUMBER, OP, STRING

from pof.utils.generator import BasicGenerator


class ExtractVariablesObfuscator:
    """Obfuscate by adding variables."""

    # BUILTINS = list(__builtins__.__dict__.keys())
    BUILTINS = (
        "__name__",
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
        "format",
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
        "super",
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

    RESERVED_WORDS = (
        "__init__",
        "__eq__",
        "__lt__",
        "append",  # on list
        "update",  # on dict
        "copy",  # copy dict or list
        "join",  # on string "".join()
        # TODO (deoktr): add all the others
    )

    RESERVED = RESERVED_WORDS + BUILTINS + tuple(keyword.kwlist)
    KEYWORDS = tuple(keyword.kwlist)

    def __init__(self, generator=None) -> None:
        if generator is None:
            generator = BasicGenerator.alphabet_generator()
        self.generator = generator

    def generate_new_name(self):
        return next(self.generator)

    def obfuscate_tokens(self, tokens):
        result = []
        new_line_buffer = []
        line_buffer = []
        parenthesis_depth = 0  # parenthesis depth
        prev_toknum = None
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            if toknum == OP and tokval == "(":
                parenthesis_depth += 1
            elif toknum == OP and tokval == ")":
                parenthesis_depth -= 1

            is_docstring = toknum == STRING and (
                prev_toknum
                in [
                    NEWLINE,
                    DEDENT,
                    INDENT,
                    ENCODING,
                ]
            )

            if (toknum == STRING and not is_docstring) or toknum == NUMBER:
                random_name = self.generate_new_name()
                new_line_buffer.extend(
                    [
                        (NEWLINE, "\n"),
                        (NAME, random_name),
                        (OP, "="),
                        *new_tokens,
                    ],
                )
                new_tokens = [(NAME, random_name)]

            # TODO (deoktr): ensure that this works
            has_decorator = any("@" in t[1] for t in line_buffer)
            newline_count = [t[1] for t in line_buffer].count("\n")

            if (
                ((toknum in (NEWLINE, NL)) and tokval == "\n") and not has_decorator
            ) or (newline_count > 1):
                if has_decorator:
                    line_buffer = [(NEWLINE, "\n"), *line_buffer]
                    new_tokens = new_line_buffer + line_buffer + new_tokens
                else:
                    new_tokens = new_line_buffer + new_tokens + line_buffer

                new_line_buffer = []
                line_buffer = []
            elif toknum in (INDENT, DEDENT):
                new_line_buffer.extend(new_tokens)
                new_tokens = None
            else:
                line_buffer.extend(new_tokens)
                new_tokens = None

            if new_tokens:
                result.extend(new_tokens)
            prev_toknum = toknum
        return result

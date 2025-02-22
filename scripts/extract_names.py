#!/bin/env python3
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

# ruff: noqa: T201
"""Extract names.

Extract names present in Python source files.
"""

import io
import keyword
import os
from tokenize import NAME, generate_tokens

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
    "self",
    "args",
    "kwargs",
)

RESERVED = RESERVED_WORDS + BUILTINS + tuple(keyword.kwlist)


class NameExtract:
    """Extract variable names from a Python source file."""

    @staticmethod
    def get_names(tokens):
        names = []
        for toknum, tokval, *_ in tokens:
            if (
                toknum == NAME
                and tokval not in RESERVED
                and tokval not in names
                and len(tokval) > 1
            ):
                names.append(tokval)
        return names

    @classmethod
    def get_from_file(cls, file):
        with file.open() as f:
            code = f.read()
        io_obj = io.StringIO(code)
        tokens = list(generate_tokens(io_obj.readline))
        return cls.get_names(tokens)


if __name__ == "__main__":
    # call with a directory containing Python source files as argument
    import sys
    from pathlib import Path

    root_path = sys.argv[1]  # ".../cpython/Lib/"
    names = []

    for dirpath, _dirnames, filenames in os.walk(root_path):
        for file in filenames:
            if not file.endswith(".py"):
                continue
            full_path = Path(dirpath) / Path(file)
            print("Checking:", full_path)
            try:
                names.extend(NameExtract.get_from_file(full_path))
            except Exception as e:  # noqa: BLE001
                print(f"Error: {e!s}")

    # filter only unique names
    print("filtering uniques")
    unames = []
    for name in names:
        if name not in unames:
            unames.append(name)

    print(f"found {len(unames)} unique names")
    with Path("out.txt").open("w") as f:
        f.write("\n".join(unames))

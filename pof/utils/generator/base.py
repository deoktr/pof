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

# TODO (deoktr): store BUILTINS in another file to share it
BUILTINS = (
    "__file__",
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


class BaseGenerator:
    RESERVED: list[str] = []  # noqa: RUF012

    @classmethod
    def extend_reserved(cls, extension):
        cls.RESERVED.extend(extension)

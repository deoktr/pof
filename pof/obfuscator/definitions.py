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

"""Definitions obfuscator.

Rename function and classes names using external package: rope
"""

# https://rope.readthedocs.io/en/latest/library.html

import ast
import io
import keyword
import shutil
from pathlib import Path
from tokenize import NAME, generate_tokens, untokenize

from pof.logger import logger
from pof.utils.generator import BasicGenerator

try:
    import rope
    from rope.base.project import Project
    from rope.refactor.rename import Rename

    ROPE_INSTALLED = True
except ImportError:
    ROPE_INSTALLED = False


class DefinitionsObfuscator:
    """Obfuscate class/function/variables names."""

    # BUILTINS = list(__builtins__.__dict__.keys())
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
        "quine",  # quine is used by pof to get the quine output
        # TODO (deoktr): add all the others
    )

    RESERVED = RESERVED_WORDS + BUILTINS + tuple(keyword.kwlist)
    KEYWORDS = keyword.kwlist

    DEFAULT_TMP_DIR = ".pof_cache"

    def __init__(self, generator=None, tmp_dir=None, *, clean=True) -> None:
        if generator is None:
            generator = BasicGenerator.alphabet_generator()
        self.generator = generator

        if tmp_dir is None:
            tmp_dir = self.DEFAULT_TMP_DIR
        self.tmp_dir = tmp_dir

        self.clean = clean

    @classmethod
    def get_local(cls, tokens):
        declared = []
        prev_tokval = None
        for _index, (toknum, tokval, *_) in enumerate(tokens):
            if (
                toknum == NAME
                and prev_tokval in ["def", "class"]
                and tokval not in cls.RESERVED_WORDS
            ):
                declared.append(tokval)
            prev_tokval = tokval
        return declared

    def list_vars(self, tokens, imports):
        var_list = []
        for toknum, tokval, _start, _end, _line in tokens:
            if (
                toknum == NAME
                and tokval not in var_list
                and tokval not in self.RESERVED
                and tokval not in imports
            ):
                var_list.append(tokval)
        return var_list

    @classmethod
    def get_imports(cls, tokens):
        source = untokenize(tokens)
        tree = ast.parse(source)
        import_list = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    import_list.append(n.name)  # noqa: PERF401
            elif isinstance(node, ast.ImportFrom):
                for n in node.names:
                    import_name = n.asname if n.asname is not None else n.name
                    import_list.append(import_name)
        return import_list

    def generate_new_name(self):
        return next(self.generator)

    def create_tmp_dir(self):
        root = Path()
        tmp_dir_path = root / self.tmp_dir
        if not tmp_dir_path.is_dir():
            tmp_dir_path.mkdir()

    def create_tmp_file(self, tokens, file_name):
        file_full_name = file_name + ".py"
        tmp_file_path = Path(self.tmp_dir) / file_full_name
        code = untokenize(tokens)
        with tmp_file_path.open("w") as f:
            f.write(code)
        return tmp_file_path

    def clean_tmp_dir(self):
        root = Path()
        tmp_dir_path = root / self.tmp_dir
        if tmp_dir_path.is_dir():
            shutil.rmtree(tmp_dir_path)

    def obfuscate_tokens(self, tokens):
        """Definitions obfuscation tokens."""
        if not ROPE_INSTALLED:
            logger.error(
                "'rope' is not installed, cannot obfuscate with DefinitionsObfuscator",
            )
            return tokens

        local_names = self.get_local(tokens)

        logger.debug(f"found {len(local_names)} local names")

        self.create_tmp_dir()

        mod_name = "tmp"
        tmp_file_path = self.create_tmp_file(tokens, mod_name)

        # TODO (deoktr): find a way better way, do everything in memory
        project = Project(self.tmp_dir)
        mod = project.get_module(mod_name)

        todo = len(local_names)
        for done, name in enumerate(local_names):
            new_name = self.generate_new_name()
            logger.debug(f"{done + 1}/{todo} renaming {name} to {new_name}")
            try:
                old_name = mod.get_attribute(name)
                pymod, lineno = old_name.get_definition_location()
                # pymod.logical_lines.logical_line_in(lineno)
                offset = pymod.resource.read().index(
                    old_name.pyobject.get_name(),
                    pymod.lines.get_line_start(lineno),
                )
                renamer = Rename(project, pymod.get_resource(), offset)
                change = renamer.get_changes(new_name)
                project.do(change)
            except (
                # can happen on class functions
                rope.base.exceptions.AttributeNotFoundError,
                # this can happen if the function is not called for example and
                # for other very obscure reasons
                ValueError,
            ):
                logger.error(f"error trying to obfuscate var {name}")
            except Exception as e:  # noqa: BLE001
                logger.exception(f"error trying to obfuscate var {name}: {e!s}")

        project.close()

        # finish by reading the file one last time
        with tmp_file_path.open() as f:
            io_obj = io.StringIO(f.read())
            tokens = list(generate_tokens(io_obj.readline))

        if self.clean:
            self.clean_tmp_dir()

        return tokens

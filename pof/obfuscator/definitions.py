"""Definitions obfuscator.

Rename function and classes names using external package: rope
"""

import ast
import io
import keyword
import logging
import shutil
from pathlib import Path
from tokenize import NAME, generate_tokens, untokenize

try:
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
        # TODO (deoktr): add all the others
    )

    RESERVED = RESERVED_WORDS + BUILTINS + tuple(keyword.kwlist)
    KEYWORDS = keyword.kwlist

    DEFAULT_TMP_DIR = ".pof_cache"

    def __init__(self, generator=None, tmp_dir=None, *, clean=False) -> None:
        if generator is None:
            from pof.utils.generator import BasicGenerator

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
        next_tokval = None
        next_toknum = None
        for index, (toknum, tokval, *_) in enumerate(tokens):
            next_tokval = None
            if len(tokens) > index + 1:
                next_toknum, next_tokval, *__ = tokens[index + 1]
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
            logging.error(
                "'rope' is not installed, cannot obfuscate with DefinitionsObfuscator",
            )
            return tokens

        local_names = self.get_local(tokens)

        msg = f"found {len(local_names)} local names"
        logging.debug(msg)

        self.create_tmp_dir()

        mod_name = "tmp"
        tmp_file_path = self.create_tmp_file(tokens, mod_name)

        # TODO (deoktr): find a way better way, do everything in memory
        proj = Project(self.tmp_dir)
        mod = proj.get_module(mod_name)

        todo = len(local_names)
        for done, name in enumerate(local_names):
            new_name = self.generate_new_name()
            msg = f"{done}/{todo} changing var {name} to {new_name}"
            logging.debug(msg)
            try:
                old_name = mod.get_attribute(name)

                pymod, lineno = old_name.get_definition_location()
                lineno_start, lineno_end = pymod.logical_lines.logical_line_in(lineno)

                offset = pymod.resource.read().index(
                    old_name.pyobject.get_name(),
                    pymod.lines.get_line_start(lineno),
                )

                changes = Rename(proj, pymod.get_resource(), offset).get_changes(
                    new_name,
                )

                proj.do(changes)
            except Exception:  # noqa: S110 BLE001
                pass
                # msg = f"error trying to obfuscate var {name}: {exc!s}"
                # logging.exception(msg)
        proj.close()

        # finish by reading the file one last time
        with tmp_file_path.open() as f:
            io_obj = io.StringIO(f.read())
            tokens = list(generate_tokens(io_obj.readline))

        if self.clean:
            self.clean_tmp_dir()

        return tokens

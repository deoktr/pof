#
# Definitions obfuscator using external package: rope
# rename function and classes names.
#
import ast
import io
import keyword
import logging
import os
from tokenize import NAME, generate_tokens, untokenize

from rope.base.project import Project
from rope.refactor.rename import Rename


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
        # TODO (204): add all the others
    )

    RESERVED = RESERVED_WORDS + BUILTINS + tuple(keyword.kwlist)
    KEYWORDS = keyword.kwlist

    def __init__(self, generator=None) -> None:
        if generator is None:
            from pof.utils.generator import BasicGenerator

            generator = BasicGenerator.alphabet_generator()
        self.generator = generator

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
                    import_list.append(n.name)
            elif isinstance(node, ast.ImportFrom):
                for n in node.names:
                    import_name = n.asname if n.asname is not None else n.name
                    import_list.append(import_name)
        return import_list

    def generate_new_name(self):
        return next(self.generator)

    def obfuscate_tokens(self, tokens):
        """Name obfuscation tokens.

        TODO (204): Obfuscate `getattr` when calling a function/variable name
        TODO (204): Obfuscate imports `import foo as bar`.
        """
        local_names = self.get_local(tokens)

        msg = f"found {len(local_names)} local names"
        logging.debug(msg)

        # TODO (204): create the directory if it doesn't exist
        # TODO (204): choose a local directory
        # TODO (204): add . in front of the directory name
        # TODO (204): directory should be an option of the class
        tmp_dir = "/tmp/test"
        file_name = "tmp.py"
        tmp_file_path = os.path.join(tmp_dir, file_name)

        code = untokenize(tokens)
        with open(tmp_file_path, "w") as f:
            f.write(code)

        def _get_tokens(code):
            io_obj = io.StringIO(code)
            return list(generate_tokens(io_obj.readline))

        # TODO (204): find a way better way, do everything in memory
        proj = Project(tmp_dir)
        mod = proj.get_module(file_name.replace(".py", ""))

        todo = len(local_names)
        done = 0
        for name in local_names:
            new_name = self.generate_new_name()
            logging.debug(f"{done}/{todo} changing var {name} to {new_name}")
            try:
                try:
                    with open(tmp_file_path) as f:
                        tokens = _get_tokens(f.read())
                except OSError:
                    break
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
            except Exception as exc:
                logging.exception(f"error trying to obfuscate var {name}: {exc!s}")
            done += 1
        proj.close()

        # finish by reading the file one last time
        with open(tmp_file_path) as f:
            return _get_tokens(f.read())

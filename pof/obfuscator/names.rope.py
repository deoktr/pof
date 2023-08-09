# WORK IN PROGRESS !
#
# Names obfuscator using external package: rope
#
# TODO (204):
# - collect every names BEFORE obfuscation to be sure never to add any that
#   where present before the obfuscation, make that an option
#
# NOTES: You can't have a variable that takes the value of an import reused elsewhere
#       for example:
#       ```
#       import os
#       BASE = "/home/test/"
#       path = os.path.join(BASE, "file.txt")
#       print(path)
#       def a(path):
#           return a + ".txt"
#       a("foo")
#       ```
#       In this example you should rename either `path` from the beginning code
#       or from the function code.
#
# NOTES: You can't have variable equal to if statement with imported names
#       Example;
#       ```
#       import os
#       is_admin = os.getuid() == 0
#       ```
#       Solution:
#       ```
#       is_admin = bool(os.getuid() == 0)
#       ```
#
import ast
import io
import keyword
import logging
import os
from tokenize import NAME, NEWLINE, NL, OP, generate_tokens, untokenize

try:
    from rope.base.project import Project
    from rope.refactor.rename import Rename

    HAS_ROPE = True
except ImportError:
    HAS_ROPE = False


class NamesObfuscator:
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
    def get_local(cls, tokens, imports):
        parenthesis_depth = 0
        declared = []
        prev_tokval = None
        next_tokval = None
        next_toknum = None
        for index, (toknum, tokval, *_) in enumerate(tokens):
            next_tokval = None
            if len(tokens) > index + 1:
                next_toknum, next_tokval, *__ = tokens[index + 1]

            if toknum == OP and tokval == "(":
                parenthesis_depth += 1
            elif toknum == OP and tokval == ")":
                parenthesis_depth -= 1

            # if (
            #       toknum == NAME
            #       and prev_tokval in ["def", "class"]
            #       and tokval not in cls.RESERVED_WORDS
            # ):
            if (
                toknum == NAME
                and (
                    # either defined class or function
                    prev_tokval in ["def", "class"]
                    # or local variable (outside of function calls)
                    or (
                        next_tokval == "="
                        and parenthesis_depth == 0
                        and prev_tokval != "."
                    )
                )
                and tokval not in cls.RESERVED
                and tokval not in imports
                and tokval not in declared
            ):
                declared.append(tokval)

            # self.foo
            # add 'foo'
            if (
                next_toknum == NAME
                and tokval == "."
                and prev_tokval in declared
                # and prev_tokval == "self"
            ):
                declared.append(next_tokval)

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

    def find_var_pos(self, tokens, var):
        current_len = 1
        for toknum, tokval, start, end, _line in tokens:
            if toknum in [NEWLINE, NL]:
                current_len += end[1]
            if toknum == NAME and tokval not in self.RESERVED and tokval == var:
                return current_len + start[1]
        return None

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
        # try with it afterward
        imports = self.get_imports(tokens)
        local_names = self.get_local(tokens, imports)
        # this one is bad, was just for testing
        # local_names = self.list_vars(tokens, imports)
        logging.debug(f"found {len(local_names)} local names")

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

        # TODO (204): find a way better way, this is SO ugly, opening and closing the
        # file to get the new position is so bad... but he I got no other
        # options right now, especially not enough time
        project = Project(tmp_dir)
        file = project.get_resource(file_name)
        # TODO (204): = len(local_names)
        done = 0
        for name in local_names:
            new_name = self.generate_new_name()
            logging.debug(
                "{done}/{todo} changing var {n} to {nn}",
                extra={"don": done, "todo": todo, "n": name, "nn": new_name},
            )
            try:
                try:
                    with open(tmp_file_path) as f:
                        tokens = _get_tokens(f.read())
                except OSError:
                    break
                index = self.find_var_pos(tokens, name)
                changes = Rename(project, file, index).get_changes(new_name)
                project.do(changes)
            except Exception as exc:
                logging.exception(
                    "error trying to obfuscate var {n}: {e}",
                    extra={"n": name, "e": str(exc)},
                )
            done += 1
        project.close()

        # finish by reading the file one last time
        with open(tmp_file_path) as f:
            return _get_tokens(f.read())

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

# THIS IS A WORK IN PROGRESS !
# No dependencies names obfuscator, works for almost everything
# If you need to obfuscate names use NamesRopeObfuscator that uses rope.
#
# TODO (deoktr): collect every names BEFORE obfuscation to be sure never to add
# any that where present before the obfuscation, make that an option
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
import unicodedata
from tokenize import NAME, OP, STRING, generate_tokens, untokenize

from pof.logger import logger
from pof.utils.generator import BasicGenerator


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
        "decode",  # on string "".decode()
        "encode",  # on string "".encode()
        "__dict__",
        # TODO (deoktr): add all the others
        "quine",  # quine is used by pof to get the quine output
    )

    RESERVED = RESERVED_WORDS + BUILTINS + tuple(keyword.kwlist)
    KEYWORDS = tuple(keyword.kwlist)

    def __init__(self, generator=None) -> None:
        if generator is None:
            generator = BasicGenerator.alphabet_generator()
        self.generator = generator

    @classmethod
    def get_local(cls, tokens, imports):
        declared = []
        for toknum, tokval, *_ in tokens:
            if toknum == NAME and tokval not in cls.RESERVED and tokval not in imports:
                declared.append(tokval)
            # prev_tokval = tokval
        return declared

    @classmethod
    def fix_strings(cls, tokens, new_names):
        # check for getattr, setattr or any other that can be used to access
        # such things maybe globals()[""] and locals()[""] too and also
        # ClassName.__dict__[""]
        # TODO (deoktr): add "RESERVED_STRINGS_WORDS" to be able to disable this feature
        # for some strings
        # FIXME (deoktr): it can be "getattr.__call__" in which case the entire thing
        # wouldn't be triggered
        # FIXME (deoktr): or getattr or the __dict__ of an object
        result = []
        depth = 0  # parenthesis depth
        inside_getattr = False
        inside_getattr_depth = None
        prev_tokval = None
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]
            if toknum == OP and tokval in ["(", "["]:
                depth += 1
            elif toknum == OP and tokval in [")", "]"]:
                depth -= 1

            # TODO (deoktr): change inside_getattr context
            if inside_getattr and depth < inside_getattr_depth:
                inside_getattr_depth = None
                inside_getattr = False
            if prev_tokval in ["getattr", "setattr", "__dict__"] and not inside_getattr:
                inside_getattr_depth = depth
                inside_getattr = True

            if toknum == STRING and inside_getattr:
                # if using `getattr` then the string reference an actual
                # variable or function of Python, we need to change it has well
                # to keep the code working
                try:
                    s = eval(tokval)  # noqa: S307
                    if s in new_names:
                        new_name = new_names[s]
                        # when adding unicode variables they are first
                        # normalized, and they can't be referenced from their
                        # original unicode value using getattr, so we'll need to
                        # normalize it too
                        # https://docs.python.org/3/reference/lexical_analysis.html#identifiers
                        new_name = unicodedata.normalize("NFKC", new_name)
                        new_tokens = [(STRING, repr(new_name))]
                except Exception as exc:  # noqa: BLE001
                    logger.warning("failed to obfuscate string %s", str(exc))

            prev_tokval = tokval
            if new_tokens:
                result.extend(new_tokens)
        return result

    @classmethod
    def import_as(cls, tokens, new_names):
        # note: the imports are always obfuscated by the main loop, this is by
        # design, for ease of use. I know this is prety dirty but otherwise we
        # would have to get the full import statement inside the main loop and
        # well it would both loose it's interest to do it here, and make it
        # impossible to use ast to do the job, which is way easier to do. So
        # unless their is a really good way to know if we are inside an import
        # statement, and know if it's imported "as" and be able to easily change
        # the import name, then we do it here, like this.

        # create an "inverted" dict of new_names, to get the key from the value
        inew_names = {}
        for key, value in new_names.items():
            inew_names.update({value: key})

        # TODO (deoktr): probably need to clean stuff here, idk if it "really" works
        source = untokenize(tokens)
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    n.name = inew_names[n.name]
                    # add "as" to the import
                    n.asname = new_names[n.name]

            elif isinstance(node, ast.ImportFrom):
                for n in node.names:
                    if n.asname is not None:
                        n.name = inew_names[n.name]
                        # add "as" to the import
                        n.asname = new_names[inew_names[n.asname]]
                    else:
                        n.name = inew_names[n.name]
                        # add "as" to the import
                        n.asname = new_names[n.name]

                # put back the old "from *name*" name
                node.module = inew_names[node.module]

        code = ast.unparse(tree)
        io_obj = io.StringIO(code)
        return list(generate_tokens(io_obj.readline))

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

    def get_new_name(self, new_names, name):
        if name not in new_names:
            new_name = self.generate_new_name()
            new_names.update({name: new_name})
        return new_names, new_names[name]

    def obfuscate_tokens(self, tokens):  # noqa: C901 PLR0912
        imports = self.get_imports(tokens)
        # declared = self.get_local(tokens, imports)
        # new_names = self.generate_new_names(declared)
        # return tokens

        result = []
        parenthesis_depth = 0  # parenthesis depth
        prev_tokval = None
        prev_toknum = None
        imutable_args = False
        imutable_depth = 0
        new_names = {}
        # fix included calls, imported_func(p=self.foo)
        # where `foo` if marked has 'imutable' because the func is imported
        # imutable = list()  # TODO (deoktr): ! keep list of all imutable
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            next_toknum = None
            if len(tokens) > index + 1:
                next_toknum, next_tokval, *__ = tokens[index + 1]

            if toknum == OP and tokval == "(":
                parenthesis_depth += 1
            elif toknum == OP and tokval == ")":
                parenthesis_depth -= 1

            # update imutable_args state
            if (
                toknum == NAME
                and (tokval in imports or tokval in self.RESERVED)
                and not imutable_args
                and tokval not in self.KEYWORDS
            ):
                # imutable_depth = parenthesis_depth
                # imutable_args = True

                # The code was moved at the bottom and using next_tokval instead
                # of tokval, this has been done to prevent a very strange bug
                pass
            elif (
                imutable_args
                and parenthesis_depth <= imutable_depth
                and "." not in [prev_tokval, tokval, next_tokval]
            ):
                imutable_args = False

            # update name
            if (
                toknum == NAME
                and tokval not in self.RESERVED
                # avoid changing class/imports functions of imported class
                and ((prev_tokval == "." and not imutable_args) or (prev_tokval != "."))
                and (
                    parenthesis_depth == 0
                    or (parenthesis_depth > 0 and next_tokval != "=")
                    or (
                        parenthesis_depth > 0
                        and next_tokval == "="
                        and not imutable_args
                    )
                )
            ):
                new_names, new_name = self.get_new_name(new_names, tokval)
                new_tokens = [(NAME, new_name)]

            if (  # noqa: SIM102
                not imutable_args
                and tokval == "="
                and toknum == OP
                and next_toknum == NAME
                and next_tokval in imports
                and prev_toknum == NAME
            ):
                # treat variable of imported object has imported
                # for example:
                #
                # import logging
                # file_handler=logging.FileHandler(config.DEBUG_LOG_FILE_PATH)
                # file_handler.setLevel(logging.DEBUG)
                #
                # in this case we shouldn't obfuscated `setLevel` has it's a
                # function of an imported object
                if prev_tokval not in imports:
                    imports.append(prev_tokval)

            # TODO (deoktr): find a better way ? really hard to tell
            if (  # noqa: SIM102
                toknum == NAME and prev_tokval == "as" and next_tokval == ":"
            ):
                # consider the following
                # with open(file_path) as f:
                # f is '_io.TextIOWrapper' and we can't obfuscate it's functions
                if tokval not in imports:
                    imports.append(tokval)

            # update imutable_args state
            if (
                next_toknum == NAME
                and (next_tokval in imports or next_tokval in self.RESERVED)
                and not imutable_args
                and next_tokval not in self.KEYWORDS
                # this is a quick and dirty fix for a problem I've had
                # and prev_tokval != "self"
            ):
                imutable_depth = parenthesis_depth
                imutable_args = True

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval
            prev_toknum = toknum

        result = self.fix_strings(result, new_names)
        return self.import_as(result, new_names)

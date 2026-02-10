# POF, a free and open source Python obfuscation framework.
# Copyright (C) 2022 - 2026  Deoktr
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

import ast
import io
from tokenize import generate_tokens, untokenize

from pof.logger import logger
from pof.utils.generator import BasicGenerator


class AstVarCollector(ast.NodeVisitor):
    def __init__(self, reserved=None):
        if reserved is None:
            reserved = []
        self.reserved = reserved

        self.assigned = set()
        self.globals = set()
        self.args = set()

    def is_valid(self, var) -> bool:
        return var not in self.reserved

    def visit_Global(self, node):
        var = node.names
        if not self.is_valid(var):
            return

        logger.debug("found globals variables to obfuscate: %s", var)
        self.globals.update(var)

    def visit_Name(self, node):
        if not isinstance(node.ctx, ast.Store):
            return

        var = node.id
        if not self.is_valid(var):
            return

        logger.debug("found variables names to obfuscate: %s", var)
        self.assigned.add(var)

    def visit_arg(self, node):
        self.args.add(node.arg)
        self.assigned.add(node.arg)


class AstVarRenamer(ast.NodeTransformer):
    def __init__(self, assigned, args, globals_, generator=None):
        self.rename = set(assigned) - set(args) - set(globals_)

        if generator is None:
            generator = BasicGenerator.alphabet_generator()
        self.generator = generator

        self.new_names = {}

    def generate_new_name(self):
        return next(self.generator)

    def get_new_name(self, name):
        if name not in self.new_names:
            new_name = self.generate_new_name()
            self.new_names.update({name: new_name})
        return self.new_names[name]

    def visit_Name(self, node):
        if node.id in self.rename:
            node.id = self.get_new_name(node.id)
        return node


class VariablesObfuscator:
    """Obfuscate local variables names using the AST."""

    def __init__(self, generator=None, reserved=None) -> None:
        if generator is None:
            generator = BasicGenerator.alphabet_generator()
        self.generator = generator

        if reserved is None:
            reserved = []
        self.reserved = reserved

    def obfuscate_tokens(self, tokens):
        source = untokenize(tokens)
        tree = ast.parse(source)

        vc = AstVarCollector(reserved=self.reserved)
        vc.visit(tree)

        tree = AstVarRenamer(
            vc.assigned,
            vc.args,
            vc.globals,
            generator=self.generator,
        ).visit(tree)
        ast.fix_missing_locations(tree)

        source = ast.unparse(tree)
        io_obj = io.StringIO(source)
        return list(generate_tokens(io_obj.readline))

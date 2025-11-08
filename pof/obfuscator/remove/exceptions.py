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

# Remove exception text, or replace it with a code.
# Replace text with code to still be able to use exception message on error
#       raise Exception("text...") --> raise Exception("42")
#       and log the code to text: 42: "text..."
from tokenize import NAME, OP, STRING

from pof.logger import logger


class ExceptionObfuscator:
    """Remove print statements from the code."""

    def __init__(self, add_codes=None, generator=None) -> None:
        if add_codes is None and generator is not None:
            add_codes = True
        self.add_codes = add_codes
        self.generator = generator

    def get_code(self):
        return next(self.generator)

    def obfuscate_tokens(self, tokens):  # noqa: C901
        result = []  # obfuscated tokens
        parenthesis_depth = 0  # parenthesis depth
        prev_tokval = None
        prev_toknum = None
        exception_par_depth = 0
        inside_exception = False
        is_exception = False
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _, next_tokval, *__ = tokens[index + 1]

            if toknum == OP and tokval == "(":
                parenthesis_depth += 1
            elif toknum == OP and tokval == ")":
                parenthesis_depth -= 1

            if inside_exception:
                if exception_par_depth == parenthesis_depth:
                    inside_exception = False
                else:
                    new_tokens = None

            elif (
                prev_toknum == NAME and is_exception and toknum == OP and tokval == "("
            ):
                inside_exception = True
                exception_par_depth = parenthesis_depth - 1
                is_exception = False

                if self.add_codes:
                    current_code = self.get_code()
                    new_tokens.extend([(STRING, f'"{current_code}"')])
                    logger.debug("Exception code %s --> %s", current_code, next_tokval)

            elif prev_tokval == "raise" and prev_toknum == NAME:
                is_exception = True
            else:
                # except Exception as e:
                #       raise e
                is_exception = False

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval
            prev_toknum = toknum
        return result

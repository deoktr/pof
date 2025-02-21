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

from tokenize import NAME, OP


class LoggingObfuscator:
    """Remove logging statements from the code."""

    @staticmethod
    def obfuscate_tokens(tokens):
        result = []  # obfuscated tokens
        parenthesis_depth = 0  # parenthesis depth
        prev_tokval = None
        logging_par_depth = 0
        inside_log = False
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _, next_tokval, *__ = tokens[index + 1]

            if not inside_log and toknum == NAME and tokval == "logging":
                new_tokens = None
                inside_log = True
                logging_par_depth = parenthesis_depth

            if tokval == "import" and next_tokval == "logging":
                new_tokens = None

            if inside_log:
                if logging_par_depth == parenthesis_depth and (
                    tokval not in ("(", "logging")
                    and prev_tokval not in (".", "logging")
                ):  # check if still inside log
                    inside_log = False
                else:
                    new_tokens = None

            if toknum == OP and tokval == "(":
                parenthesis_depth += 1
            elif toknum == OP and tokval == ")":
                parenthesis_depth -= 1

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval
        return result

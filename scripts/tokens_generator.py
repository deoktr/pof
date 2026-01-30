#!/bin/env python3
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

"""Tokens generator.

Generate the tokens representation from a Python source file.
"""

import io
import sys
from tokenize import (
    AMPER,
    AMPEREQUAL,
    AT,
    ATEQUAL,
    CIRCUMFLEX,
    CIRCUMFLEXEQUAL,
    COLON,
    COLONEQUAL,
    COMMA,
    COMMENT,
    DEDENT,
    DOT,
    DOUBLESLASH,
    DOUBLESLASHEQUAL,
    DOUBLESTAR,
    DOUBLESTAREQUAL,
    ELLIPSIS,
    ENDMARKER,
    EQEQUAL,
    EQUAL,
    ERRORTOKEN,
    GREATER,
    GREATEREQUAL,
    INDENT,
    LBRACE,
    LEFTSHIFT,
    LEFTSHIFTEQUAL,
    LESS,
    LESSEQUAL,
    LPAR,
    LSQB,
    MINEQUAL,
    MINUS,
    N_TOKENS,
    NAME,
    NEWLINE,
    NL,
    NOTEQUAL,
    NT_OFFSET,
    NUMBER,
    OP,
    PERCENT,
    PERCENTEQUAL,
    PLUS,
    PLUSEQUAL,
    RARROW,
    RBRACE,
    RIGHTSHIFT,
    RIGHTSHIFTEQUAL,
    RPAR,
    RSQB,
    SEMI,
    SLASH,
    SLASHEQUAL,
    SOFT_KEYWORD,
    STAR,
    STAREQUAL,
    STRING,
    TILDE,
    TYPE_COMMENT,
    TYPE_IGNORE,
    VBAR,
    VBAREQUAL,
    generate_tokens,
)

TOKENS_TABLE = {
    NAME: "NAME",
    LPAR: "LPAR",
    RPAR: "RPAR",
    OP: "OP",
    NL: "NL",
    NEWLINE: "NEWLINE",
    STRING: "STRING",
    NUMBER: "NUMBER",
    INDENT: "INDENT",
    DEDENT: "DEDENT",
    ENDMARKER: "ENDMARKER",
    LSQB: "LSQB",
    RSQB: "RSQB",
    COLON: "COLON",
    COMMA: "COMMA",
    SEMI: "SEMI",
    PLUS: "PLUS",
    MINUS: "MINUS",
    STAR: "STAR",
    SLASH: "SLASH",
    VBAR: "VBAR",
    AMPER: "AMPER",
    LESS: "LESS",
    GREATER: "GREATER",
    EQUAL: "EQUAL",
    DOT: "DOT",
    PERCENT: "PERCENT",
    LBRACE: "LBRACE",
    RBRACE: "RBRACE",
    EQEQUAL: "EQEQUAL",
    NOTEQUAL: "NOTEQUAL",
    LESSEQUAL: "LESSEQUAL",
    GREATEREQUAL: "GREATEREQUAL",
    TILDE: "TILDE",
    CIRCUMFLEX: "CIRCUMFLEX",
    LEFTSHIFT: "LEFTSHIFT",
    RIGHTSHIFT: "RIGHTSHIFT",
    DOUBLESTAR: "DOUBLESTAR",
    PLUSEQUAL: "PLUSEQUAL",
    MINEQUAL: "MINEQUAL",
    STAREQUAL: "STAREQUAL",
    SLASHEQUAL: "SLASHEQUAL",
    PERCENTEQUAL: "PERCENTEQUAL",
    AMPEREQUAL: "AMPEREQUAL",
    VBAREQUAL: "VBAREQUAL",
    CIRCUMFLEXEQUAL: "CIRCUMFLEXEQUAL",
    LEFTSHIFTEQUAL: "LEFTSHIFTEQUAL",
    RIGHTSHIFTEQUAL: "RIGHTSHIFTEQUAL",
    DOUBLESTAREQUAL: "DOUBLESTAREQUAL",
    DOUBLESLASH: "DOUBLESLASH",
    DOUBLESLASHEQUAL: "DOUBLESLASHEQUAL",
    AT: "AT",
    ATEQUAL: "ATEQUAL",
    RARROW: "RARROW",
    ELLIPSIS: "ELLIPSIS",
    COLONEQUAL: "COLONEQUAL",
    TYPE_IGNORE: "TYPE_IGNORE",
    TYPE_COMMENT: "TYPE_COMMENT",
    SOFT_KEYWORD: "SOFT_KEYWORD",
    ERRORTOKEN: "ERRORTOKEN",
    N_TOKENS: "N_TOKENS",
    NT_OFFSET: "NT_OFFSET",
    COMMENT: "COMMENT",
}


def tokens_of_tokens(tokens, indent: str = "    "):
    out = ""
    out += "[\n"
    for toknum, tokval, *_ in tokens:
        if toknum in TOKENS_TABLE:
            toknum_str = TOKENS_TABLE[toknum]
        out += f"{indent}({toknum_str}, {tokval!r}),\n"
    out += "]\n"
    return out


if __name__ == "__main__":
    import logging
    from pathlib import Path

    logger = logging.getLogger(__name__)

    file = sys.argv[1]
    logger.info("opening file {file}", args={"file": file})

    if file == "-":
        code = sys.stdin.read()
    else:
        with Path(file).open() as f:
            code = f.read()

    io_obj = io.StringIO(code)
    tokens = list(generate_tokens(io_obj.readline))
    sys.stdout.write(tokens_of_tokens(tokens))

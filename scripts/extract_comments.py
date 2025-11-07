#!/bin/env python3
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

# ruff: noqa: T201
"""Extract comments from Python source files."""

import io
import os
from tokenize import COMMENT, generate_tokens


class CommentExtract:
    """Extract comments from a Python source file."""

    @staticmethod
    def get_comments(tokens):
        comments = []
        for toknum, tokval, *_ in tokens:
            if toknum == COMMENT and tokval not in comments and len(tokval) > 1:
                comments.append(tokval)
        return comments

    @classmethod
    def get_from_file(cls, file):
        with file.open() as f:
            code = f.read()
        io_obj = io.StringIO(code)
        tokens = list(generate_tokens(io_obj.readline))
        return cls.get_comments(tokens)


if __name__ == "__main__":
    # call with a directory containing Python source files as argument
    import sys
    from pathlib import Path

    root_path = sys.argv[1]  # ".../cpython/Lib/"
    comments = []

    for dirpath, _dirnames, filenames in os.walk(root_path):
        for file in filenames:
            if not file.endswith(".py"):
                continue
            full_path = Path(dirpath) / Path(file)
            print("Checking:", full_path)
            try:
                comments.extend(CommentExtract.get_from_file(full_path))
            except Exception as e:  # noqa: BLE001
                print(f"Error: {e!s}")

    # filter only unique comments
    print("filtering uniques")
    ucomments = []
    for comment in comments:
        if comment not in ucomments:
            ucomments.append(comment)

    print(f"found {len(ucomments)} unique comments")
    with Path("out.txt").open("w") as f:
        f.write("\n".join(ucomments))

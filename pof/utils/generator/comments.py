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

"""Random comments generators."""

import random
from pathlib import Path

from .base import BaseGenerator


class CommentGenerator(BaseGenerator):
    @classmethod
    def realistic_generator(cls):
        """Random comment that can be variables."""
        # the comments.txt file was generated from the source of all Python 3.13
        # standard librairies, and the script used to generate it is present in
        # scripts/extract_comments.py
        file = Path(__file__).parent / "comments.txt"
        with file.open() as file:
            comment_list = [line.rstrip() for line in file]
        previous = []
        while True:
            comment = random.choice(comment_list)
            if not comment.startswith("#"):
                continue
            previous.append(comment)
            yield comment

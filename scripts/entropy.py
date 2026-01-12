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

"""Shannon entropy.

Calculate the Shannon entropy of a file.

- https://practicalsecurityanalytics.com/file-entropy/
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.entropy.html

from tests:
a basic entropy of a Python source code is around 4.3
when compressing the entropy is between 4.25 and 4.4
when using unicode variables the entropy is around 6.2
"""

import collections
import math
from pathlib import Path


def shanon_entropy(data: str) -> float:
    count = collections.Counter(map(ord, data))
    pk = [x / sum(count.values()) for x in count.values()]
    return -sum([p * math.log(p) / math.log(2) for p in pk])


if __name__ == "__main__":
    import sys

    file = Path(sys.argv[1])

    with file.open() as f:
        content = f.read()

    e = shanon_entropy(content)

    sys.stdout.write(f"{file} entropy: {e}\n")

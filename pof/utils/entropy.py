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

"""Shannon entropy.

- https://practicalsecurityanalytics.com/file-entropy/
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.entropy.html

from tests:
a basic entropy of a Python source code is around 4.3
when compressing the entropy is between 4.25 and 4.4
when using unicode variables the entropy is around 6.2
"""

import collections
import math


def entropy(data):
    count = collections.Counter(map(ord, data))

    pk = [x / sum(count.values()) for x in count.values()]

    base = 2

    # Shannon entropy
    return -sum([p * math.log(p) / math.log(base) for p in pk])

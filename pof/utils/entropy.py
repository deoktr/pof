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

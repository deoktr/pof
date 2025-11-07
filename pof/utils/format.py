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


import logging

try:
    import black

    BLACK_INSTALLED = True
except ImportError:
    BLACK_INSTALLED = False

from pof.errors import PofError


def black_format(src: str) -> str:
    """Format raw source code using black."""
    if not BLACK_INSTALLED:
        logging.error("'black' is not installed, cannot format using it")
        return src
    return black.format_str(src, mode=black.FileMode())

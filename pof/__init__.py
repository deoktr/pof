# POF, a free and open source Python obfuscation framework.
# Copyright (C) 2022-2024  POF Team
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

from pof.main import BaseObfuscator, Obfuscator

try:
    from importlib.metadata import version

    __version__ = version("python-obfuscation-framework")
except Exception:  # noqa: BLE001
    __version__ = "0.0.0"

__all__ = ("BaseObfuscator", "Obfuscator", "__version__")

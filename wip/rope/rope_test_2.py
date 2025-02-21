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

import rope
from rope.base.project import Project

proj = Project(".")
mod = proj.get_module("a")
name = mod.get_attribute("Hello")
pymod, lineno = name.get_definition_location()
lineno_start, lineno_end = pymod.logical_lines.logical_line_in(lineno)

offset = pymod.resource.read().index(
    name.pyobject.get_name(),
    pymod.lines.get_line_start(lineno),
)

changes = rope.refactor.rename.Rename(proj, pymod.get_resource(), offset).get_changes(
    "Hola",
)

proj.do(changes)

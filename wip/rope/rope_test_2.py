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

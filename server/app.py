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

from flask import Flask, Response, request, send_file
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from pof import Obfuscator

app = Flask(__name__)

# generate the Pygment CSS to be ready to serve it
pygment_css = HtmlFormatter().get_style_defs(".highlight")

# pof obfuscator instance to be reused for requests
obfuscator = Obfuscator()


@app.post("/")
def pof_route():
    """Basic HTTP endpoint to send and receive raw source code."""
    src = request.get_data().decode()
    return obfuscator.obfuscate(src)


@app.get("/")
def pof_index():
    """Simple webpage to use the /html endpoint."""
    return send_file("index.html")


@app.get("/pygment.css")
def pygment_style():
    """Style for the HTML formatted output of the /html endpoint."""
    return Response(pygment_css, mimetype="text/css")


@app.post("/html")
def pof_route_html():
    """HTML endpoint to send form data and receive HTML formatted code."""
    src = request.form.get("src", "")
    obf = obfuscator.obfuscate(src)
    return highlight(
        obf,
        PythonLexer(),
        HtmlFormatter(cssstyles="background: none;"),
    )


if __name__ == "__main__":
    app.run()

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
from pof.utils.format import black_format

INPUT_SIZE_LIMIT = 200 * 1024

app = Flask(__name__)

# generate the Pygment CSS to be ready to serve it
pygment_css = HtmlFormatter().get_style_defs(".highlight")

# pof obfuscator instance to be reused for requests
obfuscator = Obfuscator()


@app.post("/")
def pof_route():
    """Basic HTTP endpoint to send and receive raw source code."""
    src = request.get_data().decode()
    if len(src) > INPUT_SIZE_LIMIT:
        return "Inpt too large", 413

    return obfuscator.obfuscate(src)


@app.get("/")
def pof_index():
    """Simple webpage to use the /html endpoint."""
    return send_file("index.html")


@app.get("/pygment.css")
def pygment_style():
    """Style for the HTML formatted output of the /html endpoint."""
    return Response(pygment_css, mimetype="text/css")


def format_html_error(msg: str) -> str:
    return f'<p class="error">{msg}</p>'


@app.post("/html")
def pof_route_html():
    """HTML endpoint to send form data and receive HTML formatted code."""
    src = request.form.get("src", "")
    if len(src) > INPUT_SIZE_LIMIT:
        return format_html_error("Input too large.")

    try:
        obf = obfuscator.obfuscate(src)
    except Exception:  # noqa: BLE001
        return format_html_error("Failed to obfuscate, invalid input.")

    # TODO (deoktr): add a form option to enable format
    obf = black_format(obf)

    try:
        return highlight(
            obf,
            PythonLexer(),
            HtmlFormatter(cssstyles="background: none;"),
        )
    except Exception:  # noqa: BLE001
        # in case we fail to highlight, return the raw output
        return f'<p style="white-space: pre-wrap;">{obf}</p>'


if __name__ == "__main__":
    app.run()

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

import logging
import os

from flask import Flask, request, send_file, send_from_directory
from markupsafe import escape
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from pof import Obfuscator
from pof.utils.format import black_format

INPUT_SIZE_LIMIT = 200 * 1024

app = Flask(__name__)

logger = logging.getLogger(__name__)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# pof obfuscator instance to be reused for requests
obfuscator = Obfuscator()


@app.post("/")
def pof_route():
    """Basic HTTP endpoint to send and receive raw source code."""
    src = request.get_data().decode()
    if len(src) > INPUT_SIZE_LIMIT:
        logger.warning("input too large")
        return "Inpt too large", 413

    try:
        return obfuscator.obfuscate(src)
    except Exception:
        logger.exception("failed to obfuscate")
        return "", 500


@app.get("/")
def pof_index():
    """Simple webpage to use the /html endpoint."""
    return send_file("index.html")


def format_html_error(msg: str) -> str:
    return f'<p class="error">{msg}</p>'


@app.post("/html")
def pof_route_html():
    """HTML endpoint to send form data and receive HTML formatted code."""
    src = request.form.get("src", "")
    if len(src) > INPUT_SIZE_LIMIT:
        logger.warning("input too large")
        return format_html_error("Input too large.")

    try:
        obf = obfuscator.obfuscate(src)
    except Exception:
        logger.exception("failed to obfuscate")
        return format_html_error("Failed to obfuscate, invalid input.")

    # TODO (deoktr): add a form option to enable format
    try:
        obf = black_format(obf)
    except Exception:
        logger.exception("failed to format")

    try:
        return highlight(
            obf,
            PythonLexer(),
            HtmlFormatter(cssstyles="background: none;"),
        )
    except Exception:
        logger.exception("failed to highlight")

        # in case we fail to highlight, return non highlighted version
        return f'<p style="white-space: pre-wrap;">{escape(obf)}</p>'


@app.get("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.png")


if __name__ == "__main__":
    app.run()

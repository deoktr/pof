import logging

from flask import Blueprint, current_app, request
from markupsafe import escape
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from app.obfuscate import obfuscator_instance

from pof.utils.format import black_format

logger = logging.getLogger(__name__)

pof_bp = Blueprint("pof", __name__)


@pof_bp.post("/")
def pof_route():
    """Basic HTTP endpoint to send and receive raw source code."""
    src = request.get_data().decode()
    if len(src) > current_app.config["INPUT_SIZE_LIMIT"]:
        logger.warning("input too large")
        return "Inpt too large", 413

    try:
        return obfuscator_instance.obfuscate(src)
    except Exception:
        logger.exception("failed to obfuscate")
        return "", 500


def format_html_error(msg: str) -> str:
    return f'<p class="error">{msg}</p>'


@pof_bp.post("/html")
def pof_route_html():
    """HTML endpoint to send form data and receive HTML formatted code."""
    src = request.form.get("src", "")
    if len(src) > current_app.config["INPUT_SIZE_LIMIT"]:
        logger.warning("input too large")
        return format_html_error("Input too large.")

    try:
        obf = obfuscator_instance.run(src, request.form)
    except Exception:
        logger.exception("failed to obfuscate")
        return format_html_error("Failed to obfuscate, invalid input.")

    if (
        current_app.config["ENABLE_BLACK_FORMAT"]
        and request.form.get("format_black", "false") == "true"
    ):
        try:
            obf = black_format(obf)
        except Exception:
            logger.exception("failed to format with black")

    if current_app.config["ENABLE_PYGMENT"]:
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
    else:
        return f'<p style="white-space: pre-wrap;">{escape(obf)}</p>'

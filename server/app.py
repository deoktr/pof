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

# ruff: noqa: F405

import logging
from datetime import datetime
from pathlib import Path

from flask import Flask, request, send_file, send_from_directory
from markupsafe import escape
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from pof import Obfuscator, obfuscator
from pof.evasion import *  # noqa: F403
from pof.utils.format import black_format

INPUT_SIZE_LIMIT = 200 * 1024

app = Flask(__name__)

logger = logging.getLogger(__name__)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def obfuscation_helper(tokens, form, key, obfuscation_class):
    value = form.get(key)
    if value:
        tokens = obfuscation_class(value).obfuscate_tokens(tokens)
    return tokens


def obfuscation_bool_helper(tokens, form, key, obfuscation_class, **kwargs):
    if form.get(key) == "true":
        tokens = obfuscation_class(**kwargs).obfuscate_tokens(tokens)
    return tokens


def add_obfuscation(tokens, form):
    # remove
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_comments",
        obfuscator.CommentsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_exceptions",
        obfuscator.ExceptionObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_logging",
        obfuscator.LoggingObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_logging_remove",
        obfuscator.LoggingRemoveObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_print",
        obfuscator.PrintObfuscator,
    )

    # rename/move
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_globals",
        obfuscator.GlobalsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_builtins",
        obfuscator.BuiltinsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_constants",
        obfuscator.ConstantsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_definitions",
        obfuscator.DefinitionsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_extract_variables",
        obfuscator.ExtractVariablesObfuscator,
    )

    # some obfuscators should be ran once more here
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_imports",
        obfuscator.ImportsObfuscator,
    )

    # classic
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_names",
        obfuscator.NamesObfuscator,
    )
    # tokens = obfuscation_bool_helper(
    #     tokens,
    #     form,
    #     "obf_names_rope",
    #     obfuscator.NamesRopeObfuscator,
    # )

    # run all classic string and numbers obfuscators 3 times in a row
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_string",
        obfuscator.StringsObfuscator,
        import_b64decode=True,
        import_b85decode=True,
    )
    for _ in range(3):
        tokens = obfuscation_bool_helper(
            tokens,
            form,
            "obf_string",
            obfuscator.StringsObfuscator,
            import_b64decode=False,
            import_b85decode=False,
        )
        tokens = obfuscation_bool_helper(
            tokens,
            form,
            "obf_numbers",
            obfuscator.NumberObfuscator,
        )

    # unusual
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_docstrings",
        obfuscator.DocstringObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_call",
        obfuscator.CallObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_imports",
        obfuscator.ImportsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_doc",
        obfuscator.CharFromDocObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_tokens",
        obfuscator.TokensObfuscator,
    )

    # compression
    tokens = obfuscation_bool_helper(tokens, form, "obf_bz2", obfuscator.Bz2Obfuscator)
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_gzip",
        obfuscator.GzipObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_lzma",
        obfuscator.LzmaObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_zlib",
        obfuscator.ZlibObfuscator,
    )

    # ciphers
    tokens = obfuscation_bool_helper(tokens, form, "obf_rc4", obfuscator.RC4Obfuscator)
    # TODO (deoktr): fix
    # tokens = obfuscation_bool_helper(
    #     tokens,
    #     form,
    #     "obf_shift",
    #     obfuscator.ShiftObfuscator,
    # )
    tokens = obfuscation_bool_helper(tokens, form, "obf_xor", obfuscator.XORObfuscator)

    # encodings
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_a85",
        obfuscator.ASCII85Obfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_b16",
        obfuscator.Base16Obfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_b32",
        obfuscator.Base32Obfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_b32hex",
        obfuscator.Base32HexObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_b64",
        obfuscator.Base64Obfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_b85",
        obfuscator.Base85Obfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_binascii",
        obfuscator.BinasciiObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_snt",
        obfuscator.SpacenTabObfuscator,
    )
    # UPDATE FIRST
    # tokens = obfuscation_bool_helper(
    #     tokens,
    #     form,
    #     "obf_whitespace",
    #     obfuscator.WhitespaceObfuscator,
    # )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_ipv6encoding",
        obfuscator.IPv6Obfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_macencoding",
        obfuscator.MACObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_uuidencoding",
        obfuscator.UUIDObfuscator,
    )

    # finish
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_add_comments",
        obfuscator.AddCommentsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_add_newlines",
        obfuscator.AddNewlinesObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_indents",
        obfuscator.IndentsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_newline",
        obfuscator.NewlineObfuscator,
    )
    return tokens  # noqa: RET504


def evasion_helper(tokens, form, key, evasion_class):
    value = form.get(key)
    if value:
        tokens = evasion_class(value).add_evasion(tokens)
    return tokens


def evasion_list_helper(tokens, form, key, evasion_class):
    value = form.get(key)
    if value:
        tokens = evasion_class(value.split(",")).add_evasion(tokens)
    return tokens


def evasion_bool_helper(tokens, form, key, evasion_class):
    if form.get(key) == "true":
        tokens = evasion_class().add_evasion(tokens)
    return tokens


def evasion_datetime_helper(tokens, form, key, evasion_class):
    value = form.get(key)
    if value:
        parsed_date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")  # noqa: DTZ007
        tokens = evasion_class(parsed_date).add_evasion(tokens)
    return tokens


def add_evasion(tokens, form):
    tokens = evasion_helper(tokens, form, "eva_cpu_count_min", CPUCountEvasion)
    tokens = evasion_bool_helper(tokens, form, "eva_tracemalloc", TracemallocEvasion)
    tokens = evasion_bool_helper(tokens, form, "eva_debugger", DebuggerEvasion)
    tokens = evasion_bool_helper(tokens, form, "eva_executable_path", ExecPathEvasion)
    tokens = evasion_helper(tokens, form, "eva_exec_method", ExecMethodEvasion)
    tokens = evasion_helper(tokens, form, "eva_domain", DomainEvasion)
    tokens = evasion_helper(tokens, form, "eva_hostname", HostnameEvasion)
    tokens = evasion_helper(tokens, form, "eva_linux_uid", LinuxUIDEvasion)
    tokens = evasion_helper(tokens, form, "eva_username", UsernameEvasion)
    tokens = evasion_helper(tokens, form, "eva_linux_proc_count", LinuxProcCountEvasion)
    tokens = evasion_list_helper(
        tokens,
        form,
        "eva_directory_exist",
        DirectoryListExistEvasion,
    )
    tokens = evasion_list_helper(
        tokens,
        form,
        "eva_directory_missing",
        DirectoryListMissingEvasion,
    )
    tokens = evasion_list_helper(tokens, form, "eva_argv", ArgvEvasion)
    tokens = evasion_list_helper(tokens, form, "eva_file_exist", FileListExistEvasion)
    tokens = evasion_list_helper(
        tokens,
        form,
        "eva_file_missing",
        FileListMissingEvasion,
    )
    tokens = evasion_helper(tokens, form, "eva_tmp", TmpCountEvasion)
    tokens = evasion_helper(tokens, form, "eva_linux_ram_count", LinuxRAMCountEvasion)
    # TODO: convert to multile argumnets, or have multiple form fields?
    tokens = evasion_bool_helper(tokens, form, "eva_windows_prompt", WinPromptEvasion)
    tokens = evasion_datetime_helper(tokens, form, "eva_expire", ExpireEvasion)
    tokens = evasion_helper(tokens, form, "eva_linux_uptime", LinuxUptimeEvasion)
    tokens = evasion_bool_helper(tokens, form, "eva_utc_evasion", UTCEvasion)
    return tokens  # noqa: RET504


class HtmlFormObfuscator(Obfuscator):
    def run(self, source, form) -> str:
        tokens = self._get_tokens(source)
        tokens = add_evasion(tokens, form)
        tokens = add_obfuscation(tokens, form)
        return self._untokenize(tokens)


obfuscator_instance = HtmlFormObfuscator()


@app.post("/")
def pof_route():
    """Basic HTTP endpoint to send and receive raw source code."""
    src = request.get_data().decode()
    if len(src) > INPUT_SIZE_LIMIT:
        logger.warning("input too large")
        return "Inpt too large", 413

    try:
        return obfuscator_instance.obfuscate(src)
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
        obf = obfuscator_instance.run(src, request.form)
    except Exception:
        logger.exception("failed to obfuscate")
        return format_html_error("Failed to obfuscate, invalid input.")

    if request.form.get("format_black", "false") == "true":
        try:
            obf = black_format(obf)
        except Exception:
            logger.exception("failed to format with black")

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
    return send_from_directory(Path(app.root_path) / "static", "favicon.png")


if __name__ == "__main__":
    logger.info("starting pof server")
    app.run()

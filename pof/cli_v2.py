import argparse
import logging
import sys
import time

from pof import Obfuscator, __version__
from pof.errors import PofError
from pof.evasion import *  # noqa: F403
from pof.obfuscator import *  # noqa: F403
from pof.stager import *  # noqa: F403


handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s %(message)s\x1b[39m")

# colored logging
logging.addLevelName(logging.DEBUG, "\x1b[36m[*]")
logging.addLevelName(logging.INFO, "\x1b[32m[+]")
logging.addLevelName(logging.WARNING, "\x1b[33m[?]")
logging.addLevelName(logging.ERROR, "\x1b[31m[!]")
logging.addLevelName(logging.CRITICAL, "\x1b[31m[!!!]")

handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[handler])


class PofCliError(PofError):
    pass


class PofCliFlagError(PofError):
    def __init__(self, flag) -> None:
        self.message = f"missing flag: {flag}"

    def __str__(self):
        return self.message


def add_obfuscation(tokens, args):
    if args.obf_string:
        logging.debug("obfuscating strings")
        tokens = StringsObfuscator(
            import_b64decode=True,
            import_b85decode=True,
        ).obfuscate_tokens(tokens)
    if args.obf_builtins:
        logging.debug("obfuscating builtins")
        tokens = BuiltinsObfuscator().obfuscate_tokens(tokens)
    if args.obf_deep_encryption:
        logging.debug("obfuscating deep_encryption")
        tokens = DeepEncryptionObfuscator().obfuscate_tokens(tokens)
    if args.obf_rc4:
        logging.debug("obfuscating rc4")
        tokens = RC4Obfuscator().obfuscate_tokens(tokens)
    if args.obf_shift:
        logging.debug("obfuscating shift")
        tokens = ShiftObfuscator().obfuscate_tokens(tokens)
    if args.obf_xor:
        logging.debug("obfuscating xor")
        tokens = XORObfuscator().obfuscate_tokens(tokens)
    if args.obf_bz2:
        logging.debug("obfuscating bz2")
        tokens = Bz2Obfuscator().obfuscate_tokens(tokens)
    if args.obf_gzip:
        logging.debug("obfuscating gzip")
        tokens = GzipObfuscator().obfuscate_tokens(tokens)
    if args.obf_lzma:
        logging.debug("obfuscating lzma")
        tokens = LzmaObfuscator().obfuscate_tokens(tokens)
    if args.obf_zlib:
        logging.debug("obfuscating zlib")
        tokens = ZlibObfuscator().obfuscate_tokens(tokens)
    if args.obf_constants:
        logging.debug("obfuscating constants")
        tokens = ConstantsObfuscator().obfuscate_tokens(tokens)
    if args.obf_definitions:
        logging.debug("obfuscating definitions")
        tokens = DefinitionsObfuscator().obfuscate_tokens(tokens)
    if args.obf_a85:
        logging.debug("obfuscating a85")
        tokens = ASCII85Obfuscator().obfuscate_tokens(tokens)
    if args.obf_b16:
        logging.debug("obfuscating b16")
        tokens = Base16Obfuscator().obfuscate_tokens(tokens)
    if args.obf_b32:
        logging.debug("obfuscating b32")
        tokens = Base32Obfuscator().obfuscate_tokens(tokens)
    if args.obf_b32hex:
        logging.debug("obfuscating b32hex")
        tokens = Base32HexObfuscator().obfuscate_tokens(tokens)
    if args.obf_b64:
        logging.debug("obfuscating b64")
        tokens = Base64Obfuscator().obfuscate_tokens(tokens)
    if args.obf_b85:
        logging.debug("obfuscating b85")
        tokens = Base85Obfuscator().obfuscate_tokens(tokens)
    if args.obf_binascii:
        logging.debug("obfuscating binascii")
        tokens = BinasciiObfuscator().obfuscate_tokens(tokens)
    if args.obf_snt:
        logging.debug("obfuscating snt")
        tokens = SpacenTabObfuscator().obfuscate_tokens(tokens)
    if args.obf_call:
        logging.debug("obfuscating call")
        tokens = CallObfuscator().obfuscate_tokens(tokens)
    if args.obf_doc:
        logging.debug("obfuscating doc")
        tokens = CharFromDocObfuscator().obfuscate_tokens(tokens)
    if args.obf_globals:
        logging.debug("obfuscating globals")
        tokens = GlobalsObfuscator().obfuscate_tokens(tokens)
    if args.obf_imports:
        logging.debug("obfuscating imports")
        tokens = ImportsObfuscator().obfuscate_tokens(tokens)
    if args.obf_extract_variables:
        logging.debug("obfuscating extract_variables")
        tokens = ExtractVariablesObfuscator().obfuscate_tokens(tokens)
    if args.obf_add_comments:
        logging.debug("obfuscating add_comments")
        tokens = AddCommentsObfuscator().obfuscate_tokens(tokens)
    if args.obf_add_newlines:
        logging.debug("obfuscating add_newlines")
        tokens = AddNewlinesObfuscator().obfuscate_tokens(tokens)
    if args.obf_names:
        logging.debug("obfuscating names")
        tokens = NamesObfuscator().obfuscate_tokens(tokens)
    if args.obf_names_rope:
        logging.debug("obfuscating names_rope")
        tokens = NamesRopeObfuscator().obfuscate_tokens(tokens)
    if args.obf_numbers:
        logging.debug("obfuscating numbers")
        tokens = NumberObfuscator().obfuscate_tokens(tokens)
    if args.obf_tokens:
        logging.debug("obfuscating tokens")
        tokens = TokensObfuscator().obfuscate_tokens(tokens)
    if args.obf_comments:
        logging.debug("obfuscating comments")
        tokens = CommentsObfuscator().obfuscate_tokens(tokens)
    if args.obf_exceptions:
        logging.debug("obfuscating exceptions")
        tokens = ExceptionObfuscator().obfuscate_tokens(tokens)
    if args.obf_indents:
        logging.debug("obfuscating indents")
        tokens = IndentsObfuscator().obfuscate_tokens(tokens)
    if args.obf_logging:
        logging.debug("obfuscating logging")
        tokens = LoggingObfuscator().obfuscate_tokens(tokens)
    if args.obf_logging_remove:
        logging.debug("obfuscating logging remove")
        tokens = LoggingRemoveObfuscator().obfuscate_tokens(tokens)
    if args.obf_newline:
        logging.debug("obfuscating newline")
        tokens = NewlineObfuscator().obfuscate_tokens(tokens)
    if args.obf_print:
        logging.debug("obfuscating print")
        tokens = PrintObfuscator().obfuscate_tokens(tokens)
    if args.obf_docstrings:
        logging.debug("obfuscating docstrings")
        tokens = DocstringObfuscator().obfuscate_tokens(tokens)
    if args.obf_ipv6encoding:
        logging.debug("obfuscating ipv6encoding")
        tokens = IPv6Obfuscator().obfuscate_tokens(tokens)
    if args.obf_macencoding:
        logging.debug("obfuscating macencoding")
        tokens = MACObfuscator().obfuscate_tokens(tokens)
    if args.obf_uuidencoding:
        logging.debug("obfuscating uuidencoding")
        tokens = UUIDObfuscator().obfuscate_tokens(tokens)
    return tokens


def add_stagers(tokens, args):
    if args.stg_rc4:
        logging.debug("staging rc4")
        tokens = RC4Stager().generate_stager(tokens)
    if args.stg_download:
        logging.debug("staging download")
        tokens = DownloadStager().generate_stager(tokens)
    if args.stg_image:
        logging.debug("staging image")
        tokens = ImageStager().generate_stager(tokens)
    if args.stg_cl1pnet:
        logging.debug("staging cl1pnet")
        tokens = Cl1pNetStager().generate_stager(tokens)
    if args.stg_pastebin:
        logging.debug("staging pastebin")
        tokens = PastebinStager().generate_stager(tokens)
    if args.stg_pasters:
        logging.debug("staging pasters")
        tokens = PasteRsStager().generate_stager(tokens)
    if args.stg_quine:
        logging.debug("staging quine")
        tokens = QuineStager().generate_stager(tokens)
    return tokens


def add_evasion(tokens, args):
    if args.eva_argv:
        logging.debug("staging argv")
        tokens = ArgvEvasion(
            args.eva_argv_argv,
            args.eva_argv_position,
        ).add_evasion(tokens)
    if args.eva_cpu_count:
        logging.debug("staging cpu_count")
        tokens = CPUCountEvasion(args.eva_cpu_count_min).add_evasion(tokens)
    if args.eva_directory_exist:
        logging.debug("staging directory_exist")
        if args.eva_directory_exist_dir is None:
            raise PofCliFlagError("--eva-directory-exist-dir")
        tokens = DirectoryExistEvasion(args.eva_directory_exist_dir).add_evasion(
            tokens,
        )
    if args.eva_directory_list_exist:
        logging.debug("staging directory_list_exist")
        # TODO: split input list
        tokens = DirectoryListExistEvasion().add_evasion(tokens)
    if args.eva_directory_list_missing:
        logging.debug("staging directory_list_missing")
        # TODO: split input list
        tokens = DirectoryListMissingEvasion().add_evasion(tokens)
    if args.eva_directory_missing:
        logging.debug("staging directory_missing")
        tokens = DirectoryMissingEvasion().add_evasion(tokens)
    if args.eva_exec_method:
        logging.debug("staging exec_method")
        tokens = ExecMethodEvasion().add_evasion(tokens)
    if args.eva_executable_path:
        logging.debug("staging executable_path")
        tokens = ExecPathEvasion().add_evasion(tokens)
    if args.eva_file_exist:
        logging.debug("staging file_exist")
        tokens = FileExistEvasion().add_evasion(tokens)
    if args.eva_file_list_exist:
        logging.debug("staging file_list_exist")
        tokens = FileListExistEvasion().add_evasion(tokens)
    if args.eva_file_list_missing:
        logging.debug("staging file_list_missing")
        tokens = FileListMissingEvasion().add_evasion(tokens)
    if args.eva_file_missing:
        logging.debug("staging file_missing")
        tokens = FileMissingEvasion().add_evasion(tokens)
    if args.eva_tmp:
        logging.debug("staging tmp")
        # TODO: choose depending on target OS
        # LinuxTmpCountEvasion
        # TmpCountEvasion
        # WinTmpCountEvasion
        tokens = TmpCountEvasion(args.eva_tmp_count).add_evasion(tokens)
    if args.eva_ram_count:
        logging.debug("staging ram_count")
        tokens = LinuxRAMCountEvasion().add_evasion(tokens)
    if args.eva_debugger:
        logging.debug("staging debugger")
        tokens = DebuggerEvasion().add_evasion(tokens)
    if args.eva_tracemalloc:
        logging.debug("staging tracemalloc")
        tokens = TracemallocEvasion().add_evasion(tokens)
    if args.eva_prompt:
        logging.debug("staging prompt")
        tokens = WinPromptEvasion().add_evasion(tokens)
    if args.eva_multi:
        logging.debug("staging multi")
        tokens = MultiEvasion().add_evasion(tokens)
    if args.eva_domain:
        logging.debug("staging domain")
        tokens = DomainEvasion().add_evasion(tokens)
    if args.eva_hostname:
        logging.debug("staging hostname")
        tokens = HostnameEvasion().add_evasion(tokens)
    if args.eva_uid:
        logging.debug("staging uid")
        tokens = LinuxUIDEvasion().add_evasion(tokens)
    if args.eva_username:
        logging.debug("staging username")
        tokens = UsernameEvasion().add_evasion(tokens)
    if args.eva_proc_count:
        logging.debug("staging proc_count")
        tokens = LinuxProcCountEvasion().add_evasion(tokens)
    if args.eva_expire:
        logging.debug("staging expire")
        tokens = ExpireEvasion().add_evasion(tokens)
    if args.eva_uptime:
        logging.debug("staging uptime")
        tokens = LinuxUptimeEvasion().add_evasion(tokens)
    if args.eva_utc:
        logging.debug("staging utc")
        tokens = UTCEvasion().add_evasion(tokens)
    return tokens


class CLIObfuscator(Obfuscator):
    def run(self, source, args) -> str:
        """Execute a single obfuscator."""
        tokens = self._get_tokens(source)

        for _ in range(args.obf_count):
            tokens = add_obfuscation(tokens, args)

        tokens = add_stagers(tokens, args)
        tokens = add_evasion(tokens, args)

        if args.obf_result:
            for _ in range(args.obf_result_count):
                tokens = add_obfuscation(tokens, args)

        return self._untokenize(tokens)


def _handle(args) -> int:
    if args.version:
        print(__version__)  # noqa: T201
        return 0

    level = getattr(logging, args.logging)
    logger = logging.getLogger()
    logger.setLevel(level)

    logging.info(f"starting obfuscation of {args.input.name}")
    source = args.input.read()

    start = time.time()

    out = CLIObfuscator().run(source, args)

    end = time.time()

    time_diff = round(end - start, 4)
    logging.info(f"took: {time_diff}s")
    args.output.write(out)
    logging.info(f"successfully obfuscated {args.input.name} to {args.output.name}")
    # no errors
    return 0


def _cli() -> int:
    parser = argparse.ArgumentParser(
        description="%(prog)s CLI tool to obfuscate Python source code.",
    )
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument(
        "--raise-exceptions",
        action="store_true",
        help="raise exceptions instead of just logging them",
    )
    parser.add_argument(
        "input",
        nargs="?",  # required to be able to pipe to stdin
        help="input file",
        type=argparse.FileType("r"),
        default=sys.stdin,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output file",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )
    parser.add_argument(
        "--logging",
        help="logging level, DEBUG, INFO, ERROR, CRITICAL",
        default="INFO",
    )

    # obfuscation
    parser.add_argument("--obf-string", action="store_true")
    parser.add_argument("--obf-builtins", action="store_true")
    parser.add_argument("--obf-deep_encryption", action="store_true")
    parser.add_argument("--obf-rc4", action="store_true")
    parser.add_argument("--obf-shift", action="store_true")
    parser.add_argument("--obf-xor", action="store_true")
    parser.add_argument("--obf-bz2", action="store_true")
    parser.add_argument("--obf-gzip", action="store_true")
    parser.add_argument("--obf-lzma", action="store_true")
    parser.add_argument("--obf-zlib", action="store_true")
    parser.add_argument("--obf-constants", action="store_true")
    parser.add_argument("--obf-definitions", action="store_true")
    parser.add_argument("--obf-a85", action="store_true")
    parser.add_argument("--obf-b16", action="store_true")
    parser.add_argument("--obf-b32", action="store_true")
    parser.add_argument("--obf-b32hex", action="store_true")
    parser.add_argument("--obf-b64", action="store_true")
    parser.add_argument("--obf-b85", action="store_true")
    parser.add_argument("--obf-binascii", action="store_true")
    parser.add_argument("--obf-snt", action="store_true")
    parser.add_argument("--obf-call", action="store_true")
    parser.add_argument("--obf-doc", action="store_true")
    parser.add_argument("--obf-globals", action="store_true")
    parser.add_argument("--obf-imports", action="store_true")
    parser.add_argument("--obf-extract_variables", action="store_true")
    parser.add_argument("--obf-add_comments", action="store_true")
    parser.add_argument("--obf-add_newlines", action="store_true")
    parser.add_argument("--obf-names", action="store_true")
    parser.add_argument("--obf-names_rope", action="store_true")
    parser.add_argument("--obf-numbers", action="store_true")
    parser.add_argument("--obf-tokens", action="store_true")
    parser.add_argument("--obf-comments", action="store_true")
    parser.add_argument("--obf-exceptions", action="store_true")
    parser.add_argument("--obf-indents", action="store_true")
    parser.add_argument("--obf-logging", action="store_true")
    parser.add_argument("--obf-logging-remove", action="store_true")
    parser.add_argument("--obf-newline", action="store_true")
    parser.add_argument("--obf-print", action="store_true")
    parser.add_argument("--obf-docstrings", action="store_true")
    parser.add_argument("--obf-ipv6encoding", action="store_true")
    parser.add_argument("--obf-macencoding", action="store_true")
    parser.add_argument("--obf-uuidencoding", action="store_true")

    # stager
    parser.add_argument("--stg-rc4", action="store_true")
    parser.add_argument("--stg-download", action="store_true")
    parser.add_argument("--stg-image", action="store_true")
    parser.add_argument("--stg-cl1pnet", action="store_true")
    parser.add_argument("--stg-pastebin", action="store_true")
    parser.add_argument("--stg-pasters", action="store_true")
    parser.add_argument("--stg-quine", action="store_true")

    # evasion
    parser.add_argument("--eva-argv", action="store_true")
    parser.add_argument("--eva-argv-argv", default="argv")
    parser.add_argument("--eva-argv-position", type=int, default=1)
    parser.add_argument("--eva-cpu-count", action="store_true")
    parser.add_argument("--eva-cpu-count-min", type=int, default=2)
    parser.add_argument("--eva-directory-exist", action="store_true")
    parser.add_argument("--eva-directory-exist-dir")
    parser.add_argument("--eva-directory-list-exist", action="store_true")
    parser.add_argument("--eva-directory-list-missing", action="store_true")
    parser.add_argument("--eva-directory-missing", action="store_true")
    parser.add_argument("--eva-exec-method", action="store_true")
    parser.add_argument("--eva-executable-path", action="store_true")
    parser.add_argument("--eva-file-exist", action="store_true")
    parser.add_argument("--eva-file-list-exist", action="store_true")
    parser.add_argument("--eva-file-list-missing", action="store_true")
    parser.add_argument("--eva-file-missing", action="store_true")
    parser.add_argument("--eva-tmp", action="store_true")
    parser.add_argument("--eva-tmp-count", type=int, default=5)
    parser.add_argument("--eva-ram-count", action="store_true")
    parser.add_argument("--eva-debugger", action="store_true")
    parser.add_argument("--eva-tracemalloc", action="store_true")
    parser.add_argument("--eva-prompt", action="store_true")
    parser.add_argument("--eva-multi", action="store_true")
    parser.add_argument("--eva-domain", action="store_true")
    parser.add_argument("--eva-hostname", action="store_true")
    parser.add_argument("--eva-uid", action="store_true")
    parser.add_argument("--eva-username", action="store_true")
    parser.add_argument("--eva-proc-count", action="store_true")
    parser.add_argument("--eva-expire", action="store_true")
    parser.add_argument("--eva-uptime", action="store_true")
    parser.add_argument("--eva-utc", action="store_true")

    # control
    parser.add_argument(
        "--obf-count",
        type=int,
        default=1,
        help="number of times the obfuscation is ran",
    )
    parser.add_argument(
        "--obf-result",
        action="store_true",
        help="run obfuscation a second time at the end, after the stager and evasion",
    )
    parser.add_argument(
        "--obf-result-count",
        type=int,
        default=1,
        help="number of times the obfuscation is ran at the end",
    )

    args = parser.parse_args()

    try:
        return _handle(args)
    except Exception as e:
        logging.error(str(e))  # noqa: TRY400
        if args.raise_exceptions:
            raise
        logging.debug("use `--raise-exceptions` to see full trace back")
        return 1


if __name__ == "__main__":
    sys.exit(_cli())  # pragma: no cover

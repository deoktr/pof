"""pof (Python Obfuscator Framework)."""

import io
import logging
import random
from tokenize import generate_tokens

from pof.evasion import (
    CPUCountEvasion,
    DebuggerEvasion,
    DomainEvasion,
    ExecPathEvasion,
    ExpireEvasion,
    FileExistEvasion,
    FileListExistEvasion,
    FileListMissingEvasion,
    FileMissingEvasion,
    HostnameEvasion,
    LinuxRAMCountEvasion,
    LinuxUIDEvasion,
    TracemallocEvasion,
    UsernameEvasion,
)
from pof.obfuscator import (
    AddCommentsObfuscator,
    BuiltinsObfuscator,
    CommentsObfuscator,
    ConstantsObfuscator,
    DefinitionsObfuscator,
    DocstringObfuscator,
    ExceptionObfuscator,
    GlobalsObfuscator,
    IndentsObfuscator,
    LoggingObfuscator,
    NamesObfuscator,
    NewlineObfuscator,
    NumberObfuscator,
    PrintObfuscator,
    StringsObfuscator,
    XORObfuscator,
)
from pof.stager import ImageStager, RC4Stager
from pof.utils.cipher import RC4Cipher
from pof.utils.extract_names import NameExtract
from pof.utils.generator import AdvancedGenerator, BaseGenerator, BasicGenerator
from pof.utils.tokens import untokenize


class BaseObfuscator:
    @staticmethod
    def _get_tokens(source: str):
        if "\r" in source:
            source = source.replace("\r\n", "\n").replace("\r", "\n")
        if not source.endswith("\n"):
            source += "\n"
        io_obj = io.StringIO(source)
        return list(generate_tokens(io_obj.readline))

    @staticmethod
    def _untokenize(tokens):
        return untokenize(tokens)


class Obfuscator(BaseObfuscator):
    def obfuscate(
        self,
        source,
        *,
        remove_logs=False,
        remove_prints=False,
        remove_exceptions=False,
    ):
        """Complete chained obfuscation."""
        tokens = self._get_tokens(source)

        # get all the names and add them to the RESERVED_WORDS for the
        # generators
        reserved_words_add = NameExtract.get_names(tokens)
        BaseGenerator.extend_reserved(reserved_words_add)

        msg = f"reserved {len(tokens)} names"
        logging.info(msg)

        # clean input
        tokens = CommentsObfuscator().obfuscate_tokens(tokens)
        if remove_logs:
            # doesn't work yet !
            tokens = LoggingObfuscator().obfuscate_tokens(tokens)

        if remove_prints:
            # not 100% safe !
            tokens = PrintObfuscator().obfuscate_tokens(tokens)

        if remove_exceptions:
            # not fully tested
            ex_generator = (
                BasicGenerator.number_name_generator()
            )  # TODO (deoktr): have multiple generator !!!
            tokens = ExceptionObfuscator(
                add_codes=True,
                generator=ex_generator,
            ).obfuscate_tokens(tokens)

        tokens = DefinitionsObfuscator().obfuscate_tokens(tokens)

        # configure generator
        # generator = alphabet_generator()
        gen_dict = {
            86: AdvancedGenerator.realistic_generator(),
            10: BasicGenerator.alphabet_generator(),
            4: BasicGenerator.number_name_generator(length=random.randint(2, 5)),
        }
        generator = AdvancedGenerator.multi_generator(gen_dict)

        # core obfuscation
        tokens = ConstantsObfuscator(
            generator=generator,
            obf_number_rate=0.7,
            # obf_string_rate=0.1,
            obf_string_rate=0,  # FIXME (deoktr): when string obfuscation is enable and
            # name obfuscator comes next, the time delai of
            # http requests are very slow, idk why
            obf_builtins_rate=0.3,
        ).obfuscate_tokens(tokens)

        # FIXME (deoktr): breaks !
        # for detailed explanation just consider the following:
        #   ```
        #   import module
        #   class Bar:
        #       def __init__(self):
        #           self.foo = getattr(config, "FOO", True)
        #           module.imported.function(self.foo)
        #   ```
        # in this case the first instance of `foo` will successfully be
        # obfuscated (as it should) but then with the getattr it's marked has
        # "imported" because it's the result of a builtin function, but notice
        # that it's not a "simple" variable but rather it's a class attribute
        # and has a 'self' behind it, so if the variable is marked has imported
        # and a `.` is placed behind it, it won't be changed, this is the case
        # in the function call, which is itself imported, and thus set the
        # imported attribute for itself and all the parameters given to it
        # this is because we don't keep track of the level of the imported
        #
        # FIXME (deoktr): breaks !
        # Another problem is related to result of function, this is, ofc very
        # hard to deal with, but if a function returns an object, such has for
        # example an object of an imported class, which attribute are not
        # obfuscatable, then it breaks.
        #   ```
        #   import foo
        #   def a():
        #       return foo.bar()
        #   x = a()
        #   x.baz()
        #   ```
        # In this context, `baz` would be obfuscated, but it shouldn't because
        # the function is part of the `foo` imported module
        # tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)

        tokens = GlobalsObfuscator().obfuscate_tokens(tokens)
        tokens = BuiltinsObfuscator().obfuscate_tokens(tokens)

        b64decode_name = next(generator)
        b85decode_name = next(generator)
        string_obfuscator = StringsObfuscator(
            import_b64decode=True,
            import_b85decode=True,
            b64decode_name=b64decode_name,
            b85decode_name=b85decode_name,
        )
        tokens = string_obfuscator.obfuscate_tokens(tokens)
        string_obfuscator.import_b64decode = False
        string_obfuscator.import_b85decode = False

        for _ in range(2):
            tokens = NumberObfuscator().obfuscate_tokens(tokens)
        tokens = BuiltinsObfuscator().obfuscate_tokens(tokens)
        for _ in range(2):
            tokens = string_obfuscator.obfuscate_tokens(tokens)
        tokens = AddCommentsObfuscator().obfuscate_tokens(tokens)

        # clean output
        tokens = IndentsObfuscator().obfuscate_tokens(tokens)
        tokens = NewlineObfuscator().obfuscate_tokens(tokens)

        xor_payload = False
        if xor_payload:
            tokens = XORObfuscator().obfuscate_tokens(tokens)
            generator = BasicGenerator.alphabet_generator()
            tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)

        docstring_payload = False
        if docstring_payload:
            tokens = DocstringObfuscator().obfuscate_tokensj(tokens)
            generator = BasicGenerator.alphabet_generator()
            tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)
            tokens = BuiltinsObfuscator().obfuscate_tokens(tokens)
            tokens = StringsObfuscator(
                import_b64decode=True,
                import_b85decode=True,
                b64decode_name=b64decode_name,
                b85decode_name=b85decode_name,
            ).obfuscate_tokens(tokens)

        return self._untokenize(tokens)

    def basic(self, source):
        """Just the bare minimum obfuscation."""
        tokens = self._get_tokens(source)
        tokens = CommentsObfuscator().obfuscate_tokens(tokens)
        generator = BasicGenerator.alphabet_generator()
        tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)
        tokens = IndentsObfuscator().obfuscate_tokens(tokens)
        tokens = NewlineObfuscator().obfuscate_tokens(tokens)
        return self._untokenize(tokens)

    def full_evasion(  # noqa: C901, PLR0913, PLR0912
        self,
        source,
        hostname: str | None = None,
        username: str | None = None,
        uid=None,
        domain: str | None = None,
        file_exist=None,
        file_missing=None,
        min_cpu_count: int | None = None,
        min_ram: int | None = None,
        file_list_exist=None,
        file_list_missing=None,
        *,
        expire: bool = False,
        check_tracemalloc: bool = False,
        check_debugger: bool = False,
        check_executable_path: bool = False,
    ):
        tokens = self._get_tokens(source)

        if file_missing:
            tokens = FileMissingEvasion(file=file_missing).add_evasion(tokens)
        if min_cpu_count:
            tokens = CPUCountEvasion(min_cpu_count=min_cpu_count).add_evasion(tokens)
        if min_ram:
            tokens = LinuxRAMCountEvasion(min_ram=min_ram).add_evasion(tokens)
        if check_tracemalloc:
            tokens = TracemallocEvasion().add_evasion(tokens)
        if file_list_exist:
            from pof.evasion.utils import FILE_SYSTEM

            tokens = FileListMissingEvasion(file_list=FILE_SYSTEM).add_evasion(tokens)
        if file_exist:
            tokens = FileExistEvasion(file=file_exist).add_evasion(tokens)
        if file_list_missing:
            # TODO (deoktr): remove
            idk = ["/tmp/a", "/tmp/b"]  # noqa: S108
            tokens = FileListExistEvasion(file_list=idk).add_evasion(tokens)
        if domain:
            tokens = DomainEvasion(domain=domain).add_evasion(tokens)
        if hostname:
            tokens = HostnameEvasion(hostname=hostname).add_evasion(tokens)
        if uid:
            tokens = LinuxUIDEvasion(uid=uid).add_evasion(tokens)
        if username:
            tokens = UsernameEvasion(username=username).add_evasion(tokens)
        if expire:
            from datetime import datetime, timedelta

            over_datetime = datetime.utcnow()  # noqa: DTZ003
            under_datetime = datetime.utcnow() + timedelta(seconds=5)  # noqa: DTZ003
            tokens = ExpireEvasion(
                under_datetime=under_datetime,
                over_datetime=over_datetime,
            ).add_evasion(tokens)
        if check_executable_path:
            tokens = ExecPathEvasion().add_evasion(tokens)
        if check_debugger:
            tokens = DebuggerEvasion().add_evasion(tokens)

        return self._untokenize(tokens)

    def circles(self, source):
        tokens = self._get_tokens(source)
        generator = AdvancedGenerator.fixed_length_generator()
        tokens = CommentsObfuscator().obfuscate_tokens(tokens)
        tokens = ExceptionObfuscator(generator=generator).obfuscate_tokens(tokens)
        tokens = LoggingObfuscator(generator=generator).obfuscate_tokens(tokens)
        # FIXME (deoktr): when placed BEFORE NamesObfuscator it breaks the code
        # tokens = ConstantsObfuscator(
        #     generator=generator,
        #     obf_number_rate=1,
        #     # FIXME (deoktr): breaks if obf_string_rate=1 with NamesObfuscator
        #     obf_string_rate=0,
        #     # FIXME (deoktr): breaks if obf_builtins_rate=1 with NamesObfuscator
        #     obf_builtins_rate=0,
        # ).obfuscate_tokens(tokens)
        tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)
        tokens = ConstantsObfuscator(
            generator=generator,
            obf_number_rate=1,
            obf_string_rate=1,
            obf_builtins_rate=1,
        ).obfuscate_tokens(tokens)
        tokens = IndentsObfuscator().obfuscate_tokens(tokens)
        tokens = NewlineObfuscator().obfuscate_tokens(tokens)

        from tokenize import COMMENT, NEWLINE

        tokens = [(COMMENT, "# I love circles <3"), (NEWLINE, "\n"), *tokens]

        return self._untokenize(tokens)

    def image(self, source):
        """Encrypt and store the payload code inside an image."""
        tokens = self._get_tokens(source)
        img_in = "pof/wip/stegano/i.png"
        encoding_class = RC4Cipher()
        tokens = ImageStager(encoding_class=encoding_class).generate_stager(
            tokens,
            img_in,
        )
        return self._untokenize(tokens)

    def advanced_image(self, source):
        """Obfuscate, encrypt, and store the payload code inside an image."""
        tokens = self._get_tokens(source)
        generator = BasicGenerator.alphabet_generator()

        # obfuscate source
        tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)
        tokens = IndentsObfuscator().obfuscate_tokens(tokens)

        # stage inside image
        img_in = "pof/wip/stegano/i.png"
        encoding_class = RC4Cipher()
        tokens = ImageStager(encoding_class=encoding_class).generate_stager(
            tokens,
            img_in,
        )

        # FIXME (deoktr): break the image stager
        # obfuscate stager
        # tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)
        # tokens = IndentsObfuscator().obfuscate_tokens(tokens)

        # encrypt stager
        tokens = RC4Stager().generate_stager(tokens)

        # FIXME (deoktr): break the decryption part because set 256 to a variable
        # obfuscate decryption stager
        # tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)
        # tokens = IndentsObfuscator().obfuscate_tokens(tokens)

        return self._untokenize(tokens)

    def test(self, source):
        tokens = self._get_tokens(source)

        # generator = AdvancedGenerator.fixed_length_generator()
        # tokens = ConstantsObfuscator(generator=generator).obfuscate_tokens(tokens)

        tokens = CommentsObfuscator().obfuscate_tokens(tokens)
        # tokens = DeepEncryptionEvasion().add_evasion(tokens)  # TODO (deoktr): fix
        tokens = NamesObfuscator(
            generator=AdvancedGenerator.fixed_length_generator(),
        ).obfuscate_tokens(tokens)
        tokens = IndentsObfuscator().obfuscate_tokens(tokens)
        tokens = NewlineObfuscator().obfuscate_tokens(tokens)

        return self._untokenize(tokens)

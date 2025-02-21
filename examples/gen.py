#!/usr/bin/env python3
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

import pathlib
import random

import pof
from pof import BaseObfuscator
from pof.obfuscator import (
    BuiltinsObfuscator,
    CommentsObfuscator,
    ConstantsObfuscator,
    ExceptionObfuscator,
    GlobalsObfuscator,
    LoggingObfuscator,
    # NamesObfuscator,
    NumberObfuscator,
    PrintObfuscator,
    StringsObfuscator,
)
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
from pof.utils.extract_names import NameExtract
from pof.utils.generator import AdvancedGenerator, BaseGenerator, BasicGenerator


class ExampleObfuscator(BaseObfuscator):
    def constant_obf(self, source):
        tokens = self._get_tokens(source)
        tokens = ConstantsObfuscator().obfuscate_tokens(tokens)
        return self._untokenize(tokens)

    def custom_complete(self, source: str):
        # tokenize Python source code
        tokens = self._get_tokens(source)

        # get all the names and add them to the RESERVED_WORDS for the generators
        reserved_words_add = NameExtract.get_names(tokens)
        BaseGenerator.extend_reserved(reserved_words_add)

        # remove comments
        tokens = CommentsObfuscator().obfuscate_tokens(tokens)

        # replace logging message with reversable random code
        tokens = LoggingObfuscator().obfuscate_tokens(tokens)

        # remove print statements
        # NOTE: in this example we want to print
        # tokens = PrintObfuscator().obfuscate_tokens(tokens)

        # replace exceptions with reversable random names
        tokens = ExceptionObfuscator(
            add_codes=True,
            generator=BasicGenerator.number_name_generator(),
        ).obfuscate_tokens(tokens)

        # configure global generator
        generator = AdvancedGenerator.multi_generator(
            {
                86: AdvancedGenerator.realistic_generator(),
                10: BasicGenerator.alphabet_generator(),
                4: BasicGenerator.number_name_generator(length=random.randint(2, 5)),
            }
        )

        # extract values and function to make them constant
        tokens = ConstantsObfuscator(
            generator=generator,
            obf_number_rate=0.7,
            obf_string_rate=0.1,
            obf_builtins_rate=0.3,
        ).obfuscate_tokens(tokens)

        # FIXME: broken for the moment
        # tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)

        # obfuscate function calls by calling `globals()` instead
        tokens = GlobalsObfuscator().obfuscate_tokens(tokens)

        # obfuscate builtins in many different ways
        tokens = BuiltinsObfuscator().obfuscate_tokens(tokens)

        b64decode_name = next(generator)
        b85decode_name = next(generator)
        string_obfuscator = StringsObfuscator(
            import_b64decode=True,
            import_b85decode=True,
            b64decode_name=b64decode_name,
            b85decode_name=b85decode_name,
        )

        # obfuscate strings in many different ways
        tokens = string_obfuscator.obfuscate_tokens(tokens)

        # for futur usage of `string_obfuscator` don't re-import base64 and 85
        string_obfuscator.import_b64decode = False
        string_obfuscator.import_b85decode = False

        # obfuscate numbers twice in a row in many different ways
        for _ in range(2):
            tokens = NumberObfuscator().obfuscate_tokens(tokens)

        # obfuscate builtins once again
        tokens = BuiltinsObfuscator().obfuscate_tokens(tokens)

        # obfuscate strings two more times
        for _ in range(2):
            tokens = string_obfuscator.obfuscate_tokens(tokens)

        # and produce Python source code from tokens
        return self._untokenize(tokens)

    def evasion_basic(self, source):
        tokens = self._get_tokens(source)

        tokens = FileMissingEvasion(file="/tmp/foobar").add_evasion(tokens)
        tokens = CPUCountEvasion(min_cpu_count=2).add_evasion(tokens)
        tokens = LinuxRAMCountEvasion(min_ram=2).add_evasion(tokens)
        tokens = TracemallocEvasion().add_evasion(tokens)

        from datetime import datetime, timedelta, timezone

        tokens = ExpireEvasion(
            under_datetime=datetime.now() + timedelta(hours=5),
            over_datetime=datetime.now(),
        ).add_evasion(tokens)

        tokens = DebuggerEvasion().add_evasion(tokens)

        return self._untokenize(tokens)


def obfuscate_to_file(obf_class, func_name, source):
    out = getattr(obf_class, func_name)(source)
    file_name = func_name + ".py"
    file = pathlib.Path(__file__).parent / "out" / file_name
    with file.open("w") as f:
        f.write(out)


def run_all():
    file = pathlib.Path(__file__).parent / "source.py"
    with file.open() as f:
        source = f.read()

    # defaults from pof
    pof_obf = pof.Obfuscator()
    obfuscate_to_file(pof_obf, "basic", source)
    obfuscate_to_file(pof_obf, "obfuscate", source)
    obfuscate_to_file(pof_obf, "circles", source)

    # custom API example
    obf = ExampleObfuscator()
    obfuscate_to_file(obf, "constant_obf", source)
    obfuscate_to_file(obf, "custom_complete", source)
    obfuscate_to_file(obf, "evasion_basic", source)


if __name__ == "__main__":
    run_all()

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

# TODO (deoktr): have chunks of random sizes to more closely mimic the IPv6
import binascii
from tokenize import NAME, NUMBER, OP, STRING


class IPv6Encoding:
    """Encode the string in a list of valid IPv6."""

    IPV6_LEN = 32
    padding_byte = b"0"

    @classmethod
    def encode(cls, string):
        ipv6_list = []

        hex_string = binascii.b2a_hex(string)

        string_chunks = [
            hex_string[i : i + cls.IPV6_LEN]
            for i in range(0, len(hex_string), cls.IPV6_LEN)
        ]

        for sc in string_chunks:
            string_chunk = sc
            if len(string_chunk) < cls.IPV6_LEN:
                padding = cls.IPV6_LEN - len(string_chunk)
                # TODO (deoktr): choose this randomly (anything BUT the padding_byte)
                string_chunk += b"1"
                string_chunk += cls.padding_byte * (padding - 1)

            string_chunk = string_chunk.decode()

            ipv6_chunks = [
                string_chunk[i : i + 4] for i in range(0, len(string_chunk), 4)
            ]
            ipv6 = ":".join(ipv6_chunks)

            ipv6_list.append(ipv6)

        return ipv6_list

    @classmethod
    def encode_tokens(cls, string):
        ipv6_list = cls.encode(string)

        tokens = [(OP, "[")]
        for ipv6_element in ipv6_list:
            tokens.extend(((STRING, repr(ipv6_element)), (OP, ",")))
        tokens.append((OP, "]"))

        return tokens

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "binascii"),
        ]

    @classmethod
    def decode_tokens(cls, encoded_tokens):
        """IPv6 decode tokens.

        ```
        binascii.a2b_hex("".join(["...",]).replace(":", "").strip("0")[:-1])
        ```.
        """
        return [
            (NAME, "binascii"),
            (OP, "."),
            (NAME, "a2b_hex"),
            (OP, "("),
            (STRING, repr("")),
            (OP, "."),
            (NAME, "join"),
            (OP, "("),
            *encoded_tokens,
            (OP, ")"),
            (OP, "."),
            (NAME, "replace"),
            (OP, "("),
            (STRING, repr(":")),
            (OP, ","),
            (STRING, repr("")),
            (OP, ")"),
            (OP, "."),
            (NAME, "strip"),
            (OP, "("),
            (STRING, repr(cls.padding_byte.decode())),
            (OP, ")"),
            (OP, "["),
            (OP, ":"),
            (OP, "-"),
            (NUMBER, "1"),
            (OP, "]"),
            (OP, ")"),
        ]

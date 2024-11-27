import binascii
from tokenize import NAME, NUMBER, OP, STRING


class MACEncoding:
    """Encode the string in a list of valid MAC."""

    MAC_LEN = 12
    padding_byte = b"0"

    @classmethod
    def encode(cls, string):
        mac_list = []

        hex_string = binascii.b2a_hex(string)

        string_chunks = [
            hex_string[i : i + cls.MAC_LEN]
            for i in range(0, len(hex_string), cls.MAC_LEN)
        ]

        for sc in string_chunks:
            string_chunk = sc
            if len(string_chunk) < cls.MAC_LEN:
                padding = cls.MAC_LEN - len(string_chunk)
                # TODO (deoktr): choose this randomly (anything BUT the padding_byte)
                string_chunk += b"1"
                string_chunk += cls.padding_byte * (padding - 1)

            string_chunk = string_chunk.decode()

            mac_chunks = [
                string_chunk[i : i + 2] for i in range(0, len(string_chunk), 2)
            ]
            mac = "-".join(mac_chunks)

            mac_list.append(mac)

        return mac_list

    @classmethod
    def encode_tokens(cls, string):
        mac_list = cls.encode(string)

        tokens = [(OP, "[")]
        for mac_element in mac_list:
            tokens.extend(((STRING, repr(mac_element)), (OP, ",")))
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
        """MAC encoding decode tokens.

        ```
        binascii.a2b_hex("".join(["...",]).replace("-", "").strip("0")[:-1])
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
            (STRING, repr("-")),
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

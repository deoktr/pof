import binascii
from tokenize import NAME, NUMBER, OP, STRING

UUID_LEN = 32


class UUIDEncoding:
    """Encode the data in a list of valid UUID.

    Idea from: https://github.com/Bl4ckM1rror/FUD-UUID-Shellcode
    """

    padding_byte = b"0"

    @classmethod
    def encode(cls, string):
        uuid_list = []

        hex_string = binascii.b2a_hex(string)

        string_chunks = [
            hex_string[i : i + UUID_LEN] for i in range(0, len(hex_string), UUID_LEN)
        ]

        for string_chunk in string_chunks:
            sc = string_chunk
            if len(sc) < UUID_LEN:
                padding = UUID_LEN - len(sc)
                # TODO (204): choose this randomly (anything BUT the padding_byte)
                sc += b"1"
                sc += cls.padding_byte * (padding - 1)

            sc = sc.decode()
            uuid_chunks = [
                sc[0:8],
                sc[8:12],
                sc[12:16],
                sc[16:20],
                sc[20:],
            ]
            uuid = "-".join(uuid_chunks)

            uuid_list.append(uuid)

        return uuid_list

    @classmethod
    def encode_tokens(cls, string):
        uuid_list = cls.encode(string)

        tokens = [(OP, "[")]
        for uuid_element in uuid_list:
            tokens.append((STRING, repr(uuid_element)))
            tokens.append((OP, ","))
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
        """UUID decode tokens.

        ```
        binascii.a2b_hex("".join(["...",]).replace("-", "").strip("0")[:-1])
        ```
        """
        return [
            (NAME, "binascii"),
            (OP, "."),
            (NAME, "a2b_hex"),
            (OP, "("),
            (STRING, '""'),
            (OP, "."),
            (NAME, "join"),
            (OP, "("),
            *encoded_tokens,
            (OP, ")"),
            (OP, "."),
            (NAME, "replace"),
            (OP, "("),
            (STRING, '"-"'),
            (OP, ","),
            (STRING, '""'),
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

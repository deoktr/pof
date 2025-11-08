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

# TODO (deoktr): create a Stegano class in utils to be able to use this stager technique
# elsewhere, for example could be used to spread certain pieces of the source
# code in different images
# TODO (deoktr): spread the message in the image, and encode the "separation" between
# each bits at the beginning
# TODO (deoktr): encode a single bit within 2 bits of the image, instead of just using a
# single LSB (Least Significant Bit) use the last 2 bits and pass it through a
# modulus 2 to get a single bit:
#
# >>> 0b00 % 2
# 0
# >>> 0b10 % 2
# 0
# >>> 0b01 % 2
# 1
# >>> 0b11 % 2
# 1
#
# This method will ensure that we only need to change at most 1 bit and this
# bit can either be the last or the second last bit.
#
from tokenize import DEDENT, INDENT, NAME, NEWLINE, NUMBER, OP, STRING

from pof.logger import logger

try:
    from PIL import Image

    PIL_INSTALLED = True
except ModuleNotFoundError:
    PIL_INSTALLED = False

from pof.errors import PofError
from pof.utils.tokens import untokenize


class ImageStager:
    """Image.

    Hide code inside image, and generate the code to extract using LSB (Least
    Significant Bit) PNG encoding.

    Requirements:
    - PIL

    Todo:
    - add encoding/cipher class to choose how the code is stored
    - add ability to upload image to a sharing website, and download from URL,
      this should be done in a separate class
    - add option to hardcode the path of the image
    """

    def __init__(self, encoding_class=None) -> None:
        self.encoding_class = encoding_class

    @staticmethod
    def get_file_path_tokens():
        # TODO (deoktr): add other ways, for example hardcode the path, or base64
        # or from env vars
        return [
            (NAME, "sys"),
            (OP, "."),
            (NAME, "argv"),
            (OP, "."),
            (NAME, "pop"),
            (OP, "("),
            (NUMBER, "1"),
            (OP, ")"),
        ]

    @staticmethod
    def set_last_bit(number, last_bit):
        number_bin = bin(number)
        number_bin = number_bin[:-1] + last_bit
        return int(number_bin, 2)

    def encode(self, code, im_in, im_out):
        """Encode into image.

        Args:
            code: code to store
            im_in: path to image input
            im_out: path to image output.
        """
        msg_bin = bin(int.from_bytes(code, "big")).replace("0b", "")
        # mark the end of the message
        msg_bin += "0" * 8

        msg_len = len(msg_bin)
        msg_i = 0

        im = Image.open(im_in)
        px = im.load()

        for x in range(im.size[0]):
            for y in range(im.size[1]):
                pixels = px[x, y]
                red = pixels[0]

                red = self.set_last_bit(red, msg_bin[msg_i])

                px[x, y] = (red, *pixels[1:])

                msg_i += 1

                # modify pixels until the end of the message
                if msg_i >= msg_len:
                    im.save(im_out)
                    logger.info("output image written to: %s", im_out)
                    logger.info("run with: python3 path/to/stager.py %s", im_out)
                    return

        msg = "can't store message into the image because it's too big"
        raise PofError(msg)

    def generate_stager(self, tokens, image_input=None):
        """Generate the image stager.

        ```
        import sys
        from PIL import Image


        def decode(im_in):
            msg_bin = ""
            im = Image.open(im_in)
            px = im.load()
            for x in range(im.size[0]):
                for y in range(im.size[1]):
                    pixels = px[x, y]
                    msg_bin += bin(pixels[0])[-1]
            n = 8
            mmsg_bin = "0" + msg_bin
            chunks = [mmsg_bin[i : i + n] for i in range(0, len(mmsg_bin), n)]
            i = chunks.index("0" * 8)
            msg_bin = msg_bin[: (8 * i) - 1]
            n = int(msg_bin, 2)
            msg = n.to_bytes((n.bit_length() + 7) // 8, "big").decode()
            return ms


        exec(decode(sys.argv[1]))
        ```
        """
        if not PIL_INSTALLED:
            logger.error(
                "'pillow' is not installed, cannot user stager ImageStager",
            )
            return tokens

        code = untokenize(tokens)

        if image_input is None:
            image_input = input("path to image input: ")

        # TODO (deoktr): change that
        image_output = image_input.replace(".png", "_out.png")

        file_path_tokens = self.get_file_path_tokens()

        decode_tokens = [
            (NAME, "decode"),
            (OP, "("),
            *file_path_tokens,
            (OP, ")"),
        ]

        import_tokens = []
        definition_tokens = []
        if self.encoding_class:
            code = self.encoding_class.encode(code.encode())
            import_tokens = self.encoding_class.import_tokens()
            import_tokens.append((NEWLINE, "\n"))
            decode_tokens = self.encoding_class.decode_tokens(decode_tokens)
            if hasattr(self.encoding_class, "definition_tokens"):
                definition_tokens = self.encoding_class.definition_tokens()

        self.encode(code.encode(), im_in=image_input, im_out=image_output)

        return [
            *import_tokens,
            (NAME, "import"),
            (NAME, "sys"),
            (NEWLINE, "\n"),
            (NAME, "from"),
            (NAME, "PIL"),
            (NAME, "import"),
            (NAME, "Image"),
            (NEWLINE, "\n"),
            *definition_tokens,
            (NAME, "def"),
            (NAME, "decode"),
            (OP, "("),
            (NAME, "im_in"),
            (OP, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "    "),
            (NAME, "msg_bin"),
            (OP, "="),
            (STRING, '""'),
            (NEWLINE, "\n"),
            (NAME, "im"),
            (OP, "="),
            (NAME, "Image"),
            (OP, "."),
            (NAME, "open"),
            (OP, "("),
            (NAME, "im_in"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "px"),
            (OP, "="),
            (NAME, "im"),
            (OP, "."),
            (NAME, "load"),
            (OP, "("),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "for"),
            (NAME, "x"),
            (NAME, "in"),
            (NAME, "range"),
            (OP, "("),
            (NAME, "im"),
            (OP, "."),
            (NAME, "size"),
            (OP, "["),
            (NUMBER, "0"),
            (OP, "]"),
            (OP, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "        "),
            (NAME, "for"),
            (NAME, "y"),
            (NAME, "in"),
            (NAME, "range"),
            (OP, "("),
            (NAME, "im"),
            (OP, "."),
            (NAME, "size"),
            (OP, "["),
            (NUMBER, "1"),
            (OP, "]"),
            (OP, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "            "),
            (NAME, "pixels"),
            (OP, "="),
            (NAME, "px"),
            (OP, "["),
            (NAME, "x"),
            (OP, ","),
            (NAME, "y"),
            (OP, "]"),
            (NEWLINE, "\n"),
            (NAME, "msg_bin"),
            (OP, "+="),
            (NAME, "bin"),
            (OP, "("),
            (NAME, "pixels"),
            (OP, "["),
            (NUMBER, "0"),
            (OP, "]"),
            (OP, ")"),
            (OP, "["),
            (OP, "-"),
            (NUMBER, "1"),
            (OP, "]"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            (DEDENT, ""),
            (NAME, "n"),
            (OP, "="),
            (NUMBER, "8"),
            (NEWLINE, "\n"),
            (NAME, "mmsg_bin"),
            (OP, "="),
            (STRING, '"0"'),
            (OP, "+"),
            (NAME, "msg_bin"),
            (NEWLINE, "\n"),
            (NAME, "chunks"),
            (OP, "="),
            (OP, "["),
            (NAME, "mmsg_bin"),
            (OP, "["),
            (NAME, "i"),
            (OP, ":"),
            (NAME, "i"),
            (OP, "+"),
            (NAME, "n"),
            (OP, "]"),
            (NAME, "for"),
            (NAME, "i"),
            (NAME, "in"),
            (NAME, "range"),
            (OP, "("),
            (NUMBER, "0"),
            (OP, ","),
            (NAME, "len"),
            (OP, "("),
            (NAME, "mmsg_bin"),
            (OP, ")"),
            (OP, ","),
            (NAME, "n"),
            (OP, ")"),
            (OP, "]"),
            (NEWLINE, "\n"),
            (NAME, "i"),
            (OP, "="),
            (NAME, "chunks"),
            (OP, "."),
            (NAME, "index"),
            (OP, "("),
            (STRING, '"0"'),
            (OP, "*"),
            (NUMBER, "8"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "msg_bin"),
            (OP, "="),
            (NAME, "msg_bin"),
            (OP, "["),
            (OP, ":"),
            (OP, "("),
            (NUMBER, "8"),
            (OP, "*"),
            (NAME, "i"),
            (OP, ")"),
            (OP, "-"),
            (NUMBER, "1"),
            (OP, "]"),
            (NEWLINE, "\n"),
            (NAME, "n"),
            (OP, "="),
            (NAME, "int"),
            (OP, "("),
            (NAME, "msg_bin"),
            (OP, ","),
            (NUMBER, "2"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "msg"),
            (OP, "="),
            (NAME, "n"),
            (OP, "."),
            (NAME, "to_bytes"),
            (OP, "("),
            (OP, "("),
            (NAME, "n"),
            (OP, "."),
            (NAME, "bit_length"),
            (OP, "("),
            (OP, ")"),
            (OP, "+"),
            (NUMBER, "7"),
            (OP, ")"),
            (OP, "//"),
            (NUMBER, "8"),
            (OP, ","),
            (STRING, '"big"'),
            (OP, ")"),
            (OP, "."),
            (NAME, "decode"),
            (OP, "("),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "return"),
            (NAME, "msg"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            (NAME, "exec"),
            (OP, "("),
            *decode_tokens,
            (OP, ")"),
            (NEWLINE, "\n"),
        ]

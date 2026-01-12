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

# TODO
# - do it without using PIL !
# - spread the message in the image, and encode the "separation" between each
#   bits at the beginning
# - encode a single bit within 2 bits of the image, instead of just using a
#   single LSB (Least Significant Bit) use the last 2 bits and pass it through a
#   modulus 2 to get a single bit:
#
#       >>> 0b00 % 2
#       0
#       >>> 0b10 % 2
#       0
#       >>> 0b01 % 2
#       1
#       >>> 0b11 % 2
#       1
#
#   This method will ensure that we only need to change at most 1 bit and this
#   bit can either be the last or the second last bit.
# - even better set the last 2 bits for every colors and pass do a modulus on
#   it, so we encode a single bit on 6 bits, and will only need to change a
#   single one bit a time from 0 to 1 or 1 to 0 if and only if the result of the
#   modulus doesn't already encode what we want, example:
#
#       >>> 0b000100 % 2
#       0
#       >>> 0b000101 % 2
#       1
#       >>> 0b000110 % 2
#       0
#       >>> 0b000111 % 2
#       1
#
import logging

from PIL import Image


def set_last_bits(number, last_bit):
    number_bin = bin(number)
    number_bin = number_bin[:-1] + last_bit
    return int(number_bin, 2)


def encode(code, im_in, im_out):
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

            red = set_last_bits(red, msg_bin[msg_i])

            px[x, y] = (red, *pixels[1:])

            msg_i += 1

            # modify pixels until the end of the message
            if msg_i >= msg_len:
                im.save(im_out)
                logging.info(f"output image written to: {im_out}")
                return

    # check that before starting
    msg = "can't store message into the image because it's too big"
    raise Exception(msg)


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
    return n.to_bytes((n.bit_length() + 7) // 8, "big").decode()


if __name__ == "__main__":
    code = b"print('Hello, world!')"
    img_in = "pof/utils/stegano/tests/i.png"
    img_out = "pof/utils/stegano/tests/i_out.png"

    encode(code, img_in, img_out)

    decoded = decode(img_out)

    print(decoded)

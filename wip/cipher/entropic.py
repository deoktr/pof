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

# TODO
# The aim of "entropic" is to reduce the entropy of encrypted data, this is done
# by changing some characters to plain english (or any other) words, while using
# characters that are not part of the encrpytion process. So for example if the
# output of a cipher algorithm is:
# `ak27hf8hd8`
# we can replace the number `2` with: `"hello"`, giving us:
# `ak"hello"7hf8hd8`
# this technique of course lengthen the encrypted data, but can't have both strong
# encryption and low entropy. Also note that in this case it would be really
# easy for a program to remove the 'added' data but it needs to have the
# corresponding characters, and also note that their can be multiple
# corresponding characters and they don't neceseraly need to be known. For
# example we could say that the character `2` can be transformed (or not) to a
# word starting this the letter `h`, for example `hello` or `house`, this would
# again be really easy to remove/decode and add/encode.
#
# TLDR:
# There is multiple techniques more or less easy to implement and with more or
# less benefits in terms of reducing entropy:
# - add non random data at the end
# - replace single characters with a single word
# - replace single characters with a single word but only sometimes
# - replace single characters with one of multiple similar* words
# - replace multiple characters with one of multiple similar* words
# - re-use pattern (or create new ones) seen in the data
# - add non-random data with patterns and store the position at the end or start
#
# *similar being: sharing a common trait, for example starting with 'h'

# this is the shared table to encode/decode
import random

WORD_LIST = [
    "hello",
    "world",
    "foo",
    "bar",
    "baz",
]


def simple_encode(data, wordlist, frequency=8, separator="-"):
    new_data = ""
    for char in data:
        r = random.randint(0, 100)
        if r < frequency:
            word = random.choice(wordlist)
            new_data += separator + word + separator
        new_data += char
    return new_data


def simple_decode(data, separator="-"):
    new_data = ""
    inside_separator = False
    for char in data:
        if char == separator and not inside_separator:
            inside_separator = True
        elif char == separator and inside_separator:
            inside_separator = False
        elif not inside_separator:
            new_data += char
    return new_data


def end_encode(data, separator="-"):
    end = "a" * int(len(data) / 2)
    return data + separator + end


def end_decode(data, separator="-"):
    clean_data, _ = data.split(separator, 1)
    return clean_data


def entropy(data):
    # TODO (deoktr): import from the correct file
    import collections
    import math

    count = collections.Counter(map(ord, data))
    pk = [x / sum(count.values()) for x in count.values()]
    return round(-sum([p * math.log(p) / math.log(2) for p in pk]), 3)


if __name__ == "__main__":
    data = "abcdefghjklmnopqrstuvwxyz1234567890"

    # simple encode
    if False:
        encoded_data = simple_encode(data, wordlist=WORD_LIST)
        print(encoded_data)

        decoded_data = simple_decode(encoded_data)
        print(decoded_data)

        print("entropy data:", entropy(data))
        print("entropy encoded:", entropy(encoded_data))

    # end encode
    if True:
        encoded_data = end_encode(data)
        print(encoded_data)

        decoded_data = end_decode(encoded_data)
        print(decoded_data)

        print("entropy data:", entropy(data))
        print("entropy encoded:", entropy(encoded_data))

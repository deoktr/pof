from base64 import b64decode
from base64 import b85decode
# source file that will be obfuscated
import random
import string


def get_random_letter():
    """This is a docstring."""
    return random.choice(string.ascii_lowercase)


def get_random_name(name_len):
# this is a comment
    name=get_random_letter()
    for _ in range(name_len-1):
        name+=get_random_letter()
    return name


def present_my_pet():
    pet_name=get_random_name(8)
    message=b85decode('O?e=2Wpp5Eb0BVEZDnLSAO').decode()+pet_name
    print(message)


present_my_pet()

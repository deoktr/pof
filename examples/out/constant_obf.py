Bttq=print
fBZ=range
ywb5=8
DfO="My pet is name: "
tcsjsCoF=1
# source file that will be obfuscated
import random
import string


def get_random_letter():
    """This is a docstring."""
    return random.choice(string.ascii_lowercase)


def get_random_name(name_len):
# this is a comment
    name=get_random_letter().upper()
    for _ in fBZ(name_len-tcsjsCoF):
        name+=get_random_letter()
    return name


def present_my_pet():
    pet_name=get_random_name(ywb5)
    message=DfO+pet_name
    Bttq(message)


present_my_pet()

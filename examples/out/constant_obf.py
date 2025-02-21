xZBZL9iA=range
BJCaf7r="My pet is name: "
VhJw5lfA=8
a9Riwb6v=1
f238Nt=print
# source file that will be obfuscated
import random
import string


def get_random_letter():
    """This is a docstring."""
    return random.choice(string.ascii_lowercase)


def get_random_name(name_len):
# this is a comment
    name=get_random_letter()
    for _ in xZBZL9iA(name_len-a9Riwb6v):
        name+=get_random_letter()
    return name


def present_my_pet():
    pet_name=get_random_name(VhJw5lfA)
    message=BJCaf7r+pet_name
    f238Nt(message)


present_my_pet()

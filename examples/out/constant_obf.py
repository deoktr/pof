TB_="My pet is name: "
LoIC1lyQ=1
Mm9IyM=print
tkBdI=8
B6iSi8_=range
# source file that will be obfuscated
import random
import string


def get_random_letter():
    """This is a docstring."""
    return random.choice(string.ascii_lowercase)


def get_random_name(name_len):
# this is a comment
    name=get_random_letter().upper()
    for _ in B6iSi8_(name_len-LoIC1lyQ):
        name+=get_random_letter()
    return name


def present_my_pet():
    pet_name=get_random_name(tkBdI)
    message=TB_+pet_name
    Mm9IyM(message)


present_my_pet()

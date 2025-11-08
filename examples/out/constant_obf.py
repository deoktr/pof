SaE7t8geMY="My pet is named: "
wyDbWfJx=1
jkW7=print
zQfPsqJMN=range
vtSFdO_2jV=8
# source file that will be obfuscated
import random
import string


def get_random_letter():
    """This is a docstring."""
    return random.choice(string.ascii_lowercase)


def get_random_name(name_len):
# this is a comment
    name=get_random_letter()
    for _ in zQfPsqJMN(name_len-wyDbWfJx):
        name+=get_random_letter()
    return name


def present_my_pet():
    pet_name=get_random_name(vtSFdO_2jV)
    message=SaE7t8geMY+pet_name
    jkW7(message)


present_my_pet()

def base3encode(number: int):
    """Converts an integer to a base3 string."""
    if not isinstance(number, int):
        msg = "number must be an integer"
        raise TypeError(msg)

    alphabet = "0oO"

    base3 = ""
    sign = ""

    if number < 0:
        sign = "-"
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base3 = alphabet[i] + base3

    return sign + base3


def base3decode(number: str):
    return int(number.replace("o", "1").replace("O", "2"), 3)


if __name__ == "__main__":
    print(base3encode(12345678))
    print(base3decode("OoO0O00O000Oo00"))

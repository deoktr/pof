"""Base 36 is a base for an integer data type."""


def base36encode(number: int):
    """Converts an integer to a base36 string."""
    if not isinstance(number, int):
        msg = "number must be an integer"
        raise TypeError(msg)

    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    base36 = ""
    sign = ""

    if number < 0:
        sign = "-"
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36


def base36decode(number: str):
    return int(number, 36)


if __name__ == "__main__":
    print(base36encode(1412823931503067241))
    print(base36decode("AQF8AA0006EH"))

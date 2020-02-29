import string


def sanitize(msg: str):
    """
    Remove all non-letters and lowercase all letters
    """

    msg = msg.lower()
    return ''.join(letter for letter in msg if letter in string.ascii_lowercase)

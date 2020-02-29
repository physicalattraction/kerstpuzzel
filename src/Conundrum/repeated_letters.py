from pprint import pprint

from Conundrum.utils import sanitize


def decrypt(msg: str, repeated_letter: str) -> str:
    """
    Extract every letter after an occurrence of the repeated letter
    """

    msg = sanitize(msg)
    result = []
    remove_next = False
    for letter in msg:
        take_this = remove_next
        remove_next = letter == repeated_letter
        if take_this:
            result += letter
    return ''.join(result)


def decrypt_try_all(msg: str) -> [str]:
    msg = sanitize(msg)
    letters_to_try = sorted({letter for letter in msg})
    return {letter: decrypt(msg, letter) for letter in letters_to_try}


if __name__ == '__main__':
    # Used in Movies 4
    encrypted_msg = 'i bet pews or leisure chains can seem to stink of effort, george, under no illusions of vanity'
    pprint(decrypt_try_all(encrypted_msg))

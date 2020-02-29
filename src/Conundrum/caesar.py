import string

from Conundrum.utils import sanitize

letter_to_value = dict(zip('z' + string.ascii_lowercase, range(0, 27)))
value_to_letter = dict(zip(range(0, 27), 'z' + string.ascii_lowercase))


def encrypt(msg: str, index: int) -> str:
    msg = sanitize(msg)
    return ''.join([value_to_letter[(letter_to_value[msg_letter] + index) % 26]
                    for msg_letter in msg])


def decrypt(msg: str, index: int) -> str:
    msg = sanitize(msg)
    return ''.join([value_to_letter[(letter_to_value[msg_letter] - index) % 26]
                    for msg_letter in msg])


def decrypt_try_all(msg: str) -> [str]:
    msg = sanitize(msg)
    return [decrypt(msg, index) for index in range(26)]

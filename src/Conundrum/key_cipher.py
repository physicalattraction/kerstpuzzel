import math
import string

from Conundrum.utils import sanitize

letter_to_value = dict(zip('z' + string.ascii_lowercase, range(0, 27)))
value_to_letter = dict(zip(range(0, 27), 'z' + string.ascii_lowercase))


def encrypt(msg: str, key: str) -> str:
    msg = sanitize(msg)
    key = sanitize(key)
    repeat = int(math.ceil(len(msg) / len(key)))
    key = key * repeat
    return ''.join([value_to_letter[(letter_to_value[msg_letter] +
                                     letter_to_value[key_letter]) % 26]
                    for msg_letter, key_letter in zip(msg, key)])


def decrypt(msg: str, key: str) -> str:
    msg = sanitize(msg)
    key = sanitize(key)
    repeat = int(math.ceil(len(msg) / len(key)))
    key = key * repeat
    return ''.join([value_to_letter[(letter_to_value[msg_letter] -
                                     letter_to_value[key_letter]) % 26]
                    for msg_letter, key_letter in zip(msg, key)])


if __name__ == '__main__':
    # Used in Movies 1
    encrypted_msg = 'vhtubxxngahddsotmwi'
    guessed_key = 'psycho king kong taxi driver'
    print(decrypt(encrypted_msg, guessed_key))

    # Used in Movies 3
    decrypted_msg = 'metropolis'
    film_key = 'Close Encounters Of The Third Kind'
    print(encrypt(decrypted_msg, film_key))
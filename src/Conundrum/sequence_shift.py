import string
from typing import Iterator

from Conundrum.utils import sanitize

letter_to_value = dict(zip('z' + string.ascii_lowercase, range(0, 27)))
value_to_letter = dict(zip(range(0, 27), 'z' + string.ascii_lowercase))


def encrypt(msg: str, sequence: Iterator[int]) -> str:
    msg = sanitize(msg)
    return ''.join([value_to_letter[(letter_to_value[msg_letter] + index) % 26]
                    for msg_letter, index in zip(msg, sequence)])


def decrypt(msg: str, sequence: Iterator[int]) -> str:
    msg = sanitize(msg)
    return ''.join([value_to_letter[(letter_to_value[msg_letter] - index) % 26]
                    for msg_letter, index in zip(msg, sequence)])


def primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * n
    for i in range(3, int(n ** 0.5) + 1, 2):
        if sieve[i]:
            sieve[i * i::2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [i for i in range(3, n, 2) if sieve[i]]


if __name__ == '__main__':
    # Used in Movies 7
    encrypted_msg = 'vkjtltebclhpcknfcnc'
    sequence = primes(100)
    print(decrypt(encrypted_msg, sequence))

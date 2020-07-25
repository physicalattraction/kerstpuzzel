from itertools import combinations
from typing import Iterator

from Conundrum.utils import primes, sanitize


def chunks(msg: str, length: int) -> Iterator[str]:
    """
    Yield successive n-sized chunks from lst
    """

    for i in range(0, len(msg), length):
        yield msg[i:i + length]


def chop_message(msg: str, min_length: int = 6):
    length = len(msg)
    max_length = length // min_length
    for i in range(min_length, max_length):
        output = list(chunks(msg, i))

        # Read off front and back
        print(''.join([line[0] for line in output]))
        print(''.join([line[-1] for line in output]))

        # Print block
        # print('\n'.join(output) + '\n')


def chop_message_exact_length(msg: str):
    length = len(msg)
    p = primes(length)
    lengths = sorted(set(p).union(set(x * y for x, y in combinations(p, r=2)))
                     .union(set(x * y * z for x, y, z in combinations(p, r=3))))
    print(length)
    print(lengths)

    for i in lengths:
        # Ignore small lengths
        if i < 4 or length / i < 4:
            continue

        output = list(chunks(msg, i))

        # Reverse every odd line
        for index, x in enumerate(output):
            if index % 2 == 1:
                output[index] = x[::-1]

        # Read off front and back
        print(''.join([line[1] for line in output]))
        print(''.join([line[-1] for line in output]))

        # Print block
        # print('\n'.join(output) + '\n')


if __name__ == '__main__':
    msg = 'for our purposes proteins are one or more long chain acids, ' \
          'under an over-arching format. residues are bonded together.'
    msg = sanitize(msg, allowed_chars='.,- ')

    print(len(msg), msg)
    # chop_message_exact_length(msg)
    chop_message(msg, 4)

    'FOR OUR PURPOSES PROTEINS ARE ONE OR MORE LONG CHAIN ACIDS, UNDER AN OVER-ARCHING FORMAT. RESIDUES ARE BONDED TOGETHER.'
import json
import math
import os.path


def is_prime(n: int) -> bool:
    """
    Return wether the input argument is a prime number
    """

    if n == 2:
        return True
    if (n < 2) or (n % 2 == 0):
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))


def nth_prime(n: int) -> int:
    """
    Return the n'th prime number

    The results are cached on file, so the primes are only calculated once.
    """

    with open(os.path.join('..', 'json', 'primes.json'), 'r') as f:
        known_primes = json.loads(f.read())
    if str(n) in known_primes:
        return known_primes[str(n)]

    num = max(known_primes.values())
    while len(known_primes) < n:
        # Check if num is divisible by any prime before it
        num_is_prime = True
        for p in known_primes.values():
            # If there is no remainder dividing the number then the number is not a prime
            if num % p == 0:
                # Break to stop testing more numbers, we know it's not a prime
                num_is_prime = False
                break

        # If it is a prime, then add it to the dictionary of known primes.
        if num_is_prime:
            known_primes[str(len(known_primes) + 1)] = num

        # Don't check even numbers
        num += 2

    with open(os.path.join('..', 'json', 'primes.json'), 'w') as f:
        f.write(json.dumps(known_primes, indent=4))
    return known_primes[str(n)]


def prime_factorize(n: int) -> [int]:
    factors = []
    number = math.fabs(n)

    while number > 1:
        factor = _get_next_prime_factor(number)
        factors.append(factor)
        number /= factor

    if n < -1:  # If we'd check for < 0, -1 would give us trouble
        factors[0] = -factors[0]

    return factors


def _get_next_prime_factor(n: int) -> int:
    if n % 2 == 0:
        return 2

    # Not 'good' [also] checking non-prime numbers I guess?
    # But the alternative, creating a list of prime numbers,
    # wouldn't it be more demanding? Process of creating it.
    for x in range(3, int(math.ceil(math.sqrt(n)) + 1), 2):
        if n % x == 0:
            return x

    return int(n)

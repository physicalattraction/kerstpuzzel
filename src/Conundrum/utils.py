import string


def sanitize(msg: str, allowed_chars: str = ''):
    """
    Remove all non-letters and lowercase all letters
    """

    msg = msg.lower()
    return ''.join(letter for letter in msg if letter in string.ascii_lowercase + allowed_chars)


def primes(n: int) -> [int]:
    """
    Give the prime factorizatino of the input n
    """

    primfac = []
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            primfac.append(d)  # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
        primfac.append(n)
    return primfac

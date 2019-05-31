from itertools import product

import string

from prime import prime_factorize


class CheckDigit:
    def __init__(self):
        self.words = ['boommarter', 'bruinvis', 'damhert', 'veldspitsmuis', 'waterspitsmuis', 'arend', 'tuimelaar',
                      'otter', 'hazelmuis']
        self.position_in_alphabet = dict(zip([letter for letter in string.ascii_lowercase], range(0, 26)))
        self.scrabble_score = {'a': 1, 'b': 3, 'c': 5, 'd': 2, 'e': 1, 'f': 4, 'g': 3, 'h': 4, 'i': 1,
                               'j': 4, 'k': 3, 'l': 3, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 2,
                               's': 2, 't': 2, 'u': 4, 'v': 4, 'w': 5, 'x': 8, 'y': 8, 'z': 4}

    def show_check_digits(self):
        for word in self.words:
            # digits = [self._method_a(word), self._method_b(word), self._solution_b(word), self._solution_c(word)]
            # print('\t'.join([str(digit).rjust(6) for digit in digits] + [word]))
            # print('{} - {}={}'.format(word.rjust(15), str(self._solution_b(word)).rjust(4), self._method_b(word)))
            print('{} - {} - {} - {}'.format(word.rjust(15), str(self._solution_b(word)).rjust(4), str(self._solution_c(word)).rjust(4), self._scrabble_value(word)))

    def _scrabble_value(self, word):
        return [self.scrabble_score[letter] for letter in word]

    def _method_a(self, word: str) -> int:
        result = 0
        for letter in word:
            result += self.position_in_alphabet[letter]
        return result

    def _solution_b(self, word):
        solution = dict(zip(self.words, [2496, 2520, 232, 5400, 6320, 132, 0, 990, 0]))
        return solution[word]

    def _method_b(self, word: str) -> int:
        solution = self._solution_b(word)
        primes = prime_factorize(solution)
        return primes

    def _solution_c(self, word: str) -> int:
        solution = dict(zip(self.words, [0, 1366, 74, 1735, 1758, 49, 0, 379, 0]))
        return solution[word]


if __name__ == '__main__':
    cd = CheckDigit()
    cd.show_check_digits()

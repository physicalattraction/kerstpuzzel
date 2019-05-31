from collections import Counter

import string

from prime import nth_prime


class LetterSelector:
    def __init__(self):
        self.grid = [
            'Beehbkea eted  lebare  n  E',
            'dgpdv lnia eontkvrlsd etZau',
            'EeaeZlmoaeih. d tjentvlstod',
            'dseioherlrertn  dena kannar',
            'nnl d avdaiera o n  lteen r',
            'g ie;nernrnd   ,avle eitfr ',
            'p  tor semaanropaoeenvh or ',
            '  dnuaennr Eadjeevnld dvaBo',
            'no,  aoSke vknoaee ndtok  e',
            'ntmjriwednvndai  aedbr B  '
        ]
        self.line = ''
        for row in self.grid:
            self.line += row

        self.total_per_row = [len(row) for row in self.grid]

        self.col = ''
        for col in range(27):
            for row in self.grid:
                try:
                    self.col += row[col]
                except IndexError:
                    # The last row has one element less
                    pass

        self.total_letters = sum(self.total_per_row)

    def filter_letters(self, msg: str) -> [str]:
        return sorted([letter for letter in msg if letter in string.ascii_letters])

    def select_every_n(self, n: int) -> (str, str):
        msg_line = ''
        msg_col = ''
        for i in range(0, self.total_letters):
            index = (i * n) % self.total_letters
            msg_line += self.line[index]
            msg_col += self.col[index]
        return msg_line, msg_col

    def select_all_primes(self):
        for i in range(1, self.total_letters+1):
            p = nth_prime(i)
            print(p)

    def frequency_analysis(self, msg: str):
        counter = Counter(msg)
        for letter in string.ascii_lowercase:
            print('{}: {}'.format(letter, counter.get(letter, 0)))
        for letter in string.ascii_uppercase:
            if letter in counter:
                print('{}: {}'.format(letter, counter[letter]))


if __name__ == '__main__':
    ls = LetterSelector()
    # for i in range(1, 269):
    #     msg_line, msg_col = ls.select_every_n(i)
    #     if msg_line[-1] == '.' or msg_col[-1] == '.':
    #         print(i)
    #         print(msg_line)
    #         print(msg_col)
    ls.select_all_primes()
    # ls.frequency_analysis(ls.line)
    # print(''.join(ls.filter_letters(ls.line)))

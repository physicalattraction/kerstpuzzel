from itertools import permutations

import string


class LetterCrossing:

    def __init__(self):
        self.rows = [
            'AEHINRTTWXXZ',
            'ADEINSTTVXXX',
            'DEJMNORTTXXX',
            'EEIKMRSSTWXX',
            'DDEOOPRRTXXX',
            'AAEGIKKQRRSZ',
            'CFHLMMQTWXYZ',
            'AACFHQSUVWWY',
            'FIIJLOORTVVX',
            'ACFGHIJLOQXY',
            'ABBFFFLLOPRX',
            'EEIIOQRTUUZZ',
            'GIKNPTUVVVXZ',
        ]

        cols_transposed = [
            'ABCAAACAAAFB',
            'FDFHEEDDEAKC',
            'IDHHFFEEEIKE',
            'IEIJFMIGHNOE',
            'IIKNGMIGLOPF',
            'JJMOLNLOQQQI',
            'KMRSOOLRTRRI',
            'LNTTOPRSWRTR',
            'ROXUPQTSXRTT',
            'SQXUTTVTXSVT',
            'XRXVVXXUYVWU',
            'XTXXWXXYZXWV',
            'ZVZXWZXZZXYX',
        ]
        self.cols = [''.join([col[index] for col in cols_transposed])
                     for index in range(len(cols_transposed[0]))]

        self.all_letters = string.ascii_uppercase

    def letter_count(self):
        for letter in self.all_letters:
            row_count = 0
            col_count = 0
            for row in self.rows:
                if letter in row:
                    row_count += 1
            for col in self.cols:
                if letter in col:
                    col_count += 1
            print('{}: {} {}'.format(letter, row_count, col_count))
        print()

    def print_possible_letters(self):
        for row_index, row in enumerate(self.rows, start=14):
            # print('*** {} ***'.format(row_index))
            for col_index, col in enumerate(self.cols, start=12):
                possible_letters = ''
                for letter in self.all_letters:
                    if letter in row and letter in col:
                        possible_letters += letter
                if len(possible_letters) <= 3:
                    col_letter = self.all_letters[col_index]
                    print(row_index, col_letter, possible_letters)
        print()

    def possible_cols(self):
        # TODO: Quick check to see if for some letters in the rows, there is only one (or two max) column where the
        #       letter can be placed, e.g. the Bs that I had spotted manually already.
        pass

    def permute_row_24(self):
        """
        Quick check if row 24 is easy to permute

        Answer: no, there are 2,136 correct permutations possible
        """

        row = 'AFFFLLOPRX'
        possible_outcomes = []
        for p in permutations(row):
            row = p[0] + 'B' + ''.join(p[1:]) + 'B'

            if any([letter not in self.cols[letter_index]
                    for letter_index, letter in enumerate(row)]):
                continue
            else:
                possible_outcomes.append(row)
        print(len(possible_outcomes))


if __name__ == '__main__':
    lc = LetterCrossing()
    lc.letter_count()
    lc.print_possible_letters()
    # lc.permute_row_24()

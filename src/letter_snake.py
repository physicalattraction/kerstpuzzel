from word_list import WordList

from itertools import permutations, combinations


class WordListStart:
    def __init__(self):
        self.word_list = set(WordList('dutch_words'))
        # self.clean_word_list()
        self.words_per_length = {
            length: {word for word in self.word_list if len(word) == length}
            for length in [2, 3, 4, 5, 6]
        }

    @property
    def allowed_letters(self):
        return {'A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'Y'}

    def word_is_allowed(self, word: str) -> bool:
        word = word.upper()
        return all([letter in self.allowed_letters for letter in word])

    def clean_word_list(self):
        """
        Remove all words with letters that are not allowed.

        This reduces the length of the set, and hence is not worthwhile
        """

        self.word_list = {word for word in self.word_list if self.word_is_allowed(word)}

    def is_good_start(self, word: str, max_nr_letters: int = None) -> bool:
        if max_nr_letters is None:
            max_nr_letters = len(word)
        if max_nr_letters <= 1:
            return True

        for word_length in range(2, max_nr_letters + 1):
            init_word = word[:word_length]
            if init_word not in self.word_list:
                continue

            rest_word = word[word_length:]
            if not self.is_good_start(rest_word, max_nr_letters - word_length):
                continue

            # print(word)
            return True

        return False


class Snake:
    def __init__(self):
        self.word_list = set(WordList('dutch_words'))
        self.word_list_start = WordListStart()

        self.row_contents_possibilities = [['aachi', 'alntt', 'aelrw', 'aemov', 'ansuv', 'anrst', 'aopsu', 'cceen'],
                                           ['aachi', 'alntt', 'aelrw', 'afkmy', 'ansuv', 'anrst', 'aopsu', 'cceen'],
                                           ['aachi', 'alntt', 'afitw', 'aemov', 'ansuv', 'anrst', 'aopsu', 'cceen'],
                                           ['aachi', 'alntt', 'afitw', 'afkmy', 'ansuv', 'anrst', 'aopsu', 'cceen'],
                                           ['aachi', 'bdttu', 'aelrw', 'aemov', 'ansuv', 'anrst', 'aopsu', 'cceen'],
                                           ['aachi', 'bdttu', 'aelrw', 'afkmy', 'ansuv', 'anrst', 'aopsu', 'cceen'],
                                           ['aachi', 'bdttu', 'afitw', 'aemov', 'ansuv', 'anrst', 'aopsu', 'cceen'],
                                           ['aachi', 'bdttu', 'afitw', 'afkmy', 'ansuv', 'anrst', 'aopsu', 'cceen'], ]

    def answer(self, x: [[str]] = None):
        if x is None:
            x = self.row_contents_possibilities
        letters = [
            x[0][0], x[0][1], x[0][2],
            x[1][2],
            x[2][2], x[2][1],
            x[1][1], x[1][0],
            x[2][0],
            x[3][0], x[3][1],
            x[4][1], x[4][0],
            x[5][0], x[5][1], x[5][2],
            x[6][2], x[6][1], x[6][0],
            x[7][0], x[7][1], x[7][2], x[7][3], x[7][4],
            x[6][4], x[6][3],
            x[5][3],
            x[4][3], x[4][2],
            x[3][2], x[3][3],
            x[2][3],
            x[1][3],
            x[0][3], x[0][4],
            x[1][4],
            x[2][4],
            x[3][4],
            x[4][4],
            x[5][4]
        ]
        return ''.join(letters)

    def loop_over_row_contents(self, callback):
        for row_contents in self.row_contents_possibilities:
            callback(row_contents)

    def first_nine(self, row_contents: [str]):
        for first_line in combinations(row_contents[0], 3):
            x0 = ''.join(first_line)
            for second_line in combinations(row_contents[1], 3):
                x1 = ''.join(second_line)
                for third_line in combinations(row_contents[2], 3):
                    x2 = ''.join(third_line)
                    letters = [x0 + 'XX', x1 + 'XX', x2 + 'XX'] + row_contents[3:]
                    c = self.answer(letters)[:10]
                    if self.word_list_start.is_good_start(c):
                        print('XXX', c)
                    # else:
                    #     print('YYY', c)


if __name__ == '__main__':
    wls = WordListStart()
    print(wls.is_good_start('achterall'))
    print(wls.is_good_start('achtwitbaa'))

    snake = Snake()
    snake.loop_over_row_contents(snake.first_nine)

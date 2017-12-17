import json
import mmap
import os
import re

from word_list import WordList


class Regexer:

    def __init__(self):
        self.word_list = WordList(WordList.DUTCH_WORDS)
        self.words = '||'.join(list(self.word_list))

    def find_words_with_pattern(self, pattern: str) -> [str]:
        regexp = self.pattern_to_regexp(pattern)
        return re.findall(regexp, self.words, re.IGNORECASE)

    def pattern_to_regexp(self, pattern):
        return ''.join(['[\w]*' if char == '*' else char for char in pattern])


if __name__ == '__main__':
    regexer = Regexer()
    pattern = '*{}*'.format('*'.join([letter for letter in 'DEKLNRSVY']))
    all_words = regexer.find_words_with_pattern(pattern)
    print(all_words)
    # with open(os.path.join('..', 'txt', 'originals', 'DutchMoviesPerYear.txt'), 'r') as f:
    #     movie_years = json.loads(f.read())
    # for word in sorted(all_words):
    #     print(word, movie_years[word])
    # print(len(all_words))

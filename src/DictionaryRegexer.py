import mmap
import os
import re

from word_list import WordList


class DictionaryRegexer:

    def __init__(self):
        self.words = '\n'.join(WordList(['dutch_words', 'dutch_bands', 'dutch_series']))

    def find_words_with_pattern(self, pattern: str) -> [str]:
        regexp = self.pattern_to_regexp(pattern)
        return re.findall(regexp, self.words, re.IGNORECASE)

    def pattern_to_regexp(self, pattern):
        return ''.join(['[\w]*' if char == '*' else char for char in pattern])


if __name__ == '__main__':
    dr = DictionaryRegexer()
    print(len(dr.words))
    all_words = dr.find_words_with_pattern('*z*m*e*r*l*g*e*')
    all_words = dr.find_words_with_pattern('*{}*'.format('*'.join([letter for letter in 'PALMA'])))
    for word in sorted(all_words):
        print(word)
    print(len(all_words))

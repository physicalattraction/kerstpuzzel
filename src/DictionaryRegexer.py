import mmap
import os
import re


class DictionaryRegexer:

    def __init__(self):
        filename = os.path.join('..', 'csv', 'OpenTaal-210G-woordenlijsten', 'OpenTaal-210G-basis-gekeurd.txt')
        with open(filename, 'r') as f:
            self.words = f.read()

    def find_words_with_pattern(self, pattern: str) -> [str]:
        regexp = self.pattern_to_regexp(pattern)
        return re.findall(regexp, self.words, re.IGNORECASE)

    def pattern_to_regexp(self, pattern):
        return ''.join(['[\w]*' if char == '*' else char for char in pattern])


if __name__ == '__main__':
    dr = DictionaryRegexer()
    print(len(dr.words))
    all_words = dr.find_words_with_pattern('kamer*plant')
    print(all_words)

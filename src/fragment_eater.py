from utils import clean_word
from word_list import WordList


class FragmentEater:
    def __init__(self):
        self.wordlist = WordList(['dutch_series', 'dutch_bands'])

    def find_original_for_fragment(self, fragment: str) -> [(str, str)]:
        return [self.fragment_eaten(original, fragment)
                for original in self.wordlist if self.fragment_eaten(original, fragment)]

    def fragment_eaten(self, original_string: str, fragment: str) -> (str, str):
        original_string = clean_word(original_string, allowed_chars=' ')
        fragment = clean_word(fragment, allowed_chars=' ')
        eaten_letters = ''
        for letter in original_string:
            if fragment[0] == letter:
                fragment = fragment[1:]
            else:
                eaten_letters += letter
            if not fragment:
                return original_string, eaten_letters
        return ''


if __name__ == '__main__':
    fe = FragmentEater()
    print(fe.find_original_for_fragment('unlim'))

import json
import os
import re
import string
from collections import defaultdict

from utils import clean_word
from word_list import WordList


class AnagramSearcher:
    def __init__(self):
        # pass
        with open(self.anagram_index_file, 'r') as f:
            self.anagrams = json.loads(f.read())

    @property
    def word_list_file(self):
        return os.path.join('..', 'txt', 'dutch_words.txt')

    @property
    def anagram_index_file(self):
        return os.path.join('..', 'txt', 'anagram_index.txt')

    def find_anagrams_for(self, word: str) -> [str]:
        cleaned_word = clean_word(word)
        key = ''.join(sorted(cleaned_word))
        return self.anagrams.get(key, [])

    def index_anagrams_simple(self):
        """
        Call this function once to index anagrams
        """

        wordlist = WordList(['dutch_series', 'dutch_words'])
        result = defaultdict(list)
        for word in wordlist:
            word = clean_word(word)  # remove spaces
            key = ''.join(sorted(word))
            if word not in result[key]:
                result[key].append(word)
        with open(self.anagram_index_file, 'w+') as f:
            print('Creating/updating file {}'.format(self.anagram_index_file))
            f.write(json.dumps(result, indent=4))

        # After writing the file, immediately read it in memory
        with open(self.anagram_index_file, 'r') as f:
            self.anagrams = json.loads(f.read())

    def index_anagrams_multi(self):
        # TODO: Index multi word anagrams
        pass

    def remove_word_from_word(self, word_to_remove: str, total_word: str) -> str:
        word_to_remove = clean_word(word_to_remove)
        total_word = clean_word(total_word)
        for letter in word_to_remove:
            total_word = re.sub(letter, '', total_word, count=1)
        print(total_word)
        return total_word

    def clean_word_list(self):
        # TODO: Move to WordList
        filename = os.path.join('..', 'csv', 'OpenTaal-210G-woordenlijsten', 'OpenTaal-210G-basis-gekeurd.txt')
        with open(filename, 'r') as f:
            words = f.read().split('\n')
        words = [clean_word(word) for word in words]
        with open(self.word_list_file, 'w+') as f:
            f.write('\n'.join(words))

    def new_letter(self, number: int, letter: str):
        # TODO: Move away from anagram_searcher
        letter_to_number = {letter: i + 1 for i, letter in enumerate(string.ascii_lowercase)}
        print(letter_to_number)
        number_to_letter = {i + 1: letter for i, letter in enumerate(string.ascii_lowercase)}
        new_number = number - letter_to_number[letter.lower()]
        return number_to_letter[new_number].upper()


if __name__ == '__main__':
    anagrams = AnagramSearcher()
    # anagrams.clean_word_list()
    # anagrams.index_anagrams_simple()

    dutch_bands = WordList(['dutch_bands'])
    for band in dutch_bands:
        found_anagrams = anagrams.find_anagrams_for(band)
        found_anagrams = [anagram for anagram in found_anagrams if anagram != band]
        if found_anagrams:
            print('{} - {}'.format(band, ', '.join(found_anagrams)))


import json
import os
import re
import string
from collections import defaultdict

from utils import clean_word
from word_list import WordList


class AnagramSearcher:
    def __init__(self):
        if os.path.exists(self.anagram_index_file):
            with open(self.anagram_index_file, 'r') as f:
                self.anagrams = json.loads(f.read())
        else:
            self.anagrams = {}

    @property
    def anagram_index_file(self):
        return os.path.join('..', 'txt', 'anagram_index.json')

    def find_anagrams_for(self, word: str) -> [str]:
        cleaned_word = clean_word(word)
        key = ''.join(sorted(cleaned_word))
        return self.anagrams.get(key, [])

    def find_anagrams_with_extra_letters_for(self, word: str):
        found_anagrams = set()
        for extra_letter in ' ' + string.ascii_lowercase:
            new_word = word + extra_letter
            for extra_letter in ' ' + string.ascii_lowercase:
                new_word = new_word + extra_letter
                for extra_letter in ' ' + string.ascii_lowercase:
                    new_word = new_word + extra_letter
                    for found_anagram in self.find_anagrams_for(new_word):
                        found_anagrams.add(found_anagram)
        return found_anagrams

    def index_anagrams_simple(self, word_list: WordList = None):
        """
        Call this function once to index anagrams
        """

        result = self.anagrams
        for word in word_list:
            word = clean_word(word)  # remove spaces
            key = ''.join(sorted(word))
            if key not in result:
                result[key] = []
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
        return total_word

    def new_letter(self, number: int, letter: str):
        # TODO: Move away from anagram_searcher
        letter_to_number = {letter: i + 1 for i, letter in enumerate(string.ascii_lowercase)}
        print(letter_to_number)
        number_to_letter = {i + 1: letter for i, letter in enumerate(string.ascii_lowercase)}
        new_number = number - letter_to_number[letter.lower()]
        return number_to_letter[new_number].upper()


if __name__ == '__main__':
    anagram_searcher = AnagramSearcher()
    anagram_searcher.index_anagrams_simple(WordList([WordList.DUTCH_WORDS, WordList.DIED2017]))

    # dutch_bands = WordList(['dutch_bands'])
    # for band in dutch_bands:
    #     found_anagrams = anagram_searcher.find_anagrams_for(band)
    #     found_anagrams = [anagram for anagram in found_anagrams if anagram != band]
    #     if found_anagrams:
    #         print('{} - {}'.format(band, ', '.join(found_anagrams)))

    words_3a = 'ABDEJRSTU FKNPS DGHIKLRT BDGHIJNPRST BGINPRSTU ABERU DEKLNRSVY'.split(' ')
    words_25b = 'Banjo Praal Scene, Kan Chip Gein, Nar Cijfer Knik, Tribunes Eigenaar Snoei, Gel Daar Lint, ' \
                'Coup Cru Ze, Fok Zo Kamer, Kweekte Wie Ooit, Alias Vilt Veer, Nachtmis Nulde Dun, ' \
                'Vaan Durven Cacao, Leesvaardigheid Helpen Pitten, Rem Standaard Melden, Omtrent Nerd Daalder, ' \
                'Schadevergoeding Want Tennist'.split(', ')
    for word in words_25b:
        anagrams = anagram_searcher.find_anagrams_with_extra_letters_for(word)
        print('{}: {}'.format(word, anagrams or '-'))

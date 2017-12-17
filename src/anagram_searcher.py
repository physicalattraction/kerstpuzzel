import json
import os
import re
import string
from collections import defaultdict
from itertools import permutations, combinations

import math

from utils import clean_word
from word_list import WordList

MIN_LENGTH = 2


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

    def find_anagrams_multi_for(self, word: str) -> [str]:
        result = []
        cleaned_word = clean_word(word)
        half_length = int(len(cleaned_word) / 2)
        min_length = max(half_length, MIN_LENGTH - 1)
        for word_length in range(len(cleaned_word), min_length, -1):
            for combination in combinations(cleaned_word, word_length):
                key = ''.join(sorted(combination))
                anagrams = self.anagrams.get(key, [])
                if anagrams:
                    left_word = self.remove_word_from_word(key, cleaned_word)
                    if len(left_word) >= MIN_LENGTH:
                        anagrams_from_left_word = self.find_anagrams_multi_for(left_word)
                        if anagrams_from_left_word:
                            for current_anagram in anagrams:
                                for anagram_from_left_word in anagrams_from_left_word:
                                    result.append('{} {}'.format(current_anagram, anagram_from_left_word))
                    elif len(left_word) == 0:
                        result += anagrams
        return sorted(set(result))

    def find_anagrams_with_extra_letters_for(self, word: str) -> [str]:
        # TODO: Use permutations and search for words as partial anagrams and continue from rest of word iteratively
        found_anagrams = set()
        for extra_letter_1 in ' ' + string.ascii_lowercase:
            for extra_letter_2 in ' ' + string.ascii_lowercase:
                for extra_letter_3 in ' ' + string.ascii_lowercase:
                    new_word = word + extra_letter_1 + extra_letter_2 + extra_letter_3
                    for found_anagram in self.find_anagrams_for(new_word):
                        found_anagrams.add(found_anagram)
        return sorted(found_anagrams)

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

    def remove_word_from_word(self, word_to_remove: str, total_word: str) -> str:
        word_to_remove = clean_word(word_to_remove)
        total_word = clean_word(total_word)
        for letter in word_to_remove:
            total_word = re.sub(letter, '', total_word, count=1)
        return total_word

    def print_permutations(self, txt: str):
        txt = [letter for letter in txt.lower() if letter in string.ascii_lowercase]
        for index, perm in enumerate(permutations(txt)):
            print('{}: {}'.format(index, ''.join(perm)))


if __name__ == '__main__':
    anagram_searcher = AnagramSearcher()
    # anagram_searcher.index_anagrams_simple(WordList([WordList.DUTCH_MOVIES, WordList.DUTCH_BANDS]))

    result = anagram_searcher.find_anagrams_multi_for('narcijferknik')
    for word in result:
        print(word)
        if 'van' in word.split(' '):
            print(word)

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
    # for word in words_3a:
    #     anagrams = anagram_searcher.find_anagrams_with_extra_letters_for(word)
    #     anagrams = anagram_searcher.find_anagrams_for(word)
    #     print('{}: {}'.format(word, anagrams or '-'))

    # anagram_searcher.print_permutations('Coup Cru Ze')
    # word = anagram_searcher.remove_word_from_word('gitaar',
    #                                               anagram_searcher.remove_word_from_word('de', 'Gel Daar Lint'))
    # print(word)
    # anagram_searcher.find_anagrams_for(word)

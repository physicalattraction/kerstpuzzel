import json
import os
import re
import string
from itertools import permutations, combinations

from utils import clean_word
from word_list import WordList

MIN_LENGTH = 3


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
        half_length = int(len(cleaned_word) / 3)
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
                                    result.append(f'{current_anagram} {anagram_from_left_word}')
                    elif len(left_word) == 0:
                        result += anagrams
        return sorted(set(result))

    def find_anagrams_with_extra_letters_for(self, word: str, nr_extra_letters: int) -> [str]:
        found_anagrams = set()

        for permutation in permutations(' ' + string.ascii_lowercase, nr_extra_letters):
            extra_letters = ''.join(permutation)
            new_word = word + extra_letters
            for found_anagram in self.find_anagrams_multi_for(new_word):
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
            print(f'Creating/updating file {self.anagram_index_file}')
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
            perm_str = ''.join(perm)
            print(f'{index}: {perm_str}')

    def find_anagrams_for_pairs(self, list_of_words: [str]):
        word_pairs = combinations(list_of_words, 2)
        for pair in word_pairs:
            input = pair[0] + pair[1]
            anagrams = self.find_anagrams_for(input)
            if anagrams:
                print('{}: ({}) {}'.format(pair, len(anagrams), anagrams[:30]))


if __name__ == '__main__':
    anagram_searcher = AnagramSearcher()
    result = anagram_searcher.find_anagrams_multi_for('LJJSTTRTijjts')
    print(result)
    result = anagram_searcher.find_anagrams_multi_for('jamkullokmij')
    print(result)
    exit()


    # result = anagram_searcher.find_anagrams_with_extra_letters_for('BGINPRSTU', nr_extra_letters=2)
    # for word in result:
    #     split_word = word.split(' ')
    #     if len(split_word) == 3 and  'en' in split_word:
    #         print(word)

    # dutch_bands = WordList(['dutch_bands'])
    # for band in dutch_bands:
    #     found_anagrams = anagram_searcher.find_anagrams_for(band)
    #     found_anagrams = [anagram for anagram in found_anagrams if anagram != band]
    #     if found_anagrams:
    #         print('{} - {}'.format(band, ', '.join(found_anagrams)))

    words_3a = 'ABDEJRSTU FKNPS DGHIKLRT BDGHIJNPRST BGINPRSTU ABERU DEKLNRSVY'.split(' ')
    words_13 = 'EVEONZW FYNTXIZXSG NMNCVHG OLTOBVX ORDZPRE PEHRCVIGQVF VQNNNVIF YRFTRYH YVFCIVATRMT'.split(' ')
    words_25b = 'Banjo Praal Scene, Kan Chip Gein, Nar Cijfer Knik, Tribunes Eigenaar Snoei, Gel Daar Lint, ' \
                'Coup Cru Ze, Fok Zo Kamer, Kweekte Wie Ooit, Alias Vilt Veer, Nachtmis Nulde Dun, ' \
                'Vaan Durven Cacao, Leesvaardigheid Helpen Pitten, Rem Standaard Melden, Omtrent Nerd Daalder, ' \
                'Schadevergoeding Want Tennist'.split(', ')
    words_30 = 'ADAPTER, BAAS, BENDE, GENADE, LEIDEN, LENTEUI, MOLIERE, PIKKER, RICINE, RIFF, SATIRE, SCENE, SPEL, ' \
               'STAAF, TOTEBEL, VAL, VENTER'.split(', ')
    words_34c = 'BORREL, BRONS, CHIP, COOKER, DRAIN, FRISUUR, GAAR, GAVEN, KELT, LAMA, MARS, MASTINO, SMUL, TELER, ' \
                'TRASSI'.split(', ')

    # anagram_searcher.find_anagrams_for_pairs(words_34c)

    # for word in words_25b:
    #     anagrams = anagram_searcher.find_anagrams_multi_for(word)
    #     for anagram in anagrams:
    #         print('{} - {}'.format(word, anagram))
    # for word in words_3a:
    #     anagrams = anagram_searcher.find_anagrams_with_extra_letters_for(word, nr_extra_letters=4)
    #     for anagram in anagrams:
    #         print('{} - {}'.format(word, anagram))

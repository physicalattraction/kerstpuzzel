from itertools import combinations, permutations

import string
import re
from collections import Counter, defaultdict

from pprint import pprint

from word_list import WordList

msg = 'IQKAGERASZASKRZMMTWXLYHQFCAVHUWQCASYASWFXOIJFOITLRVVFJCHLAXGQOYILBFXFFLOARPBIRTZUOZEUTZIQEXITZNVPVGTZVKU'


class NollHuTonde:
    def __init__(self):
        self.msg = 'noll hu tonde tonko noll tonko tonde tongo de de go tonde tonko me la tonko ra go tonti tonko hu ' \
                   'go tonsu go la tonko me tonde tonhu tonko ti noll la tonko tonde tonti noll noll tonti tonko ' \
                   'noll tonko by go hu me ni ko tonko noll noll la tonko tonra tonko fy hu tongo tonde tonko tonme ' \
                   'tonko fy hu tongo tonde tonko tonni tonvy tonko tonby go tonan ko tonko me tonde tonko tonra ' \
                   'tonhu tonko tonme tonko me tonde tonko tonde fy go hu tonko go la tonko tonni tonko me tonde ' \
                   'tonko ni go tonko vy po la ti tonko ti me de ra tonti tonko ra po tongo ti go la tonvy'
        self.msg = '12.30 12.40 2.00 12.00 ' \
                   '1.00 1.20 3.00 12.20 ' \
                   '1.10 12.40 3.40 2.20 ' \
                   '2.20 2.50 12.30 12.40 ' \
                   '2.10 12.40 2.10 12.30 ' \
                   '12.40 1.50 12.00 2.00 ' \
                   '2.00 12.40 2.50 1.00 ' \
                   '1.20 12.40 2.50 2.30 ' \
                   '12.00 3.00 3.00 12.40 ' \
                   '2.10 12.30 1.20 3.10 ' \
                   '1.30 12.00 12.00 2.50 ' \
                   '1.20 2.10 1.10 12.40 ' \
                   '3.10 2.30 3.20 4.10 ' \
                   '4.10 12.40 1.50 3.10 ' \
                   '1.10 12.40 2.00 12.00'
        split_msg = self.msg.split(' ')
        self.words = sorted(set(split_msg))
        self.word_histogram = Counter(split_msg)
        # https://onzetaal.nl/taaladvies/letterfrequentie-in-het-nederlands
        self.letter_histogram = {
            'E': 18.91,
            'N': 10.03,
            'A': 7.49,
            'T': 6.79,
            'I': 6.50,
            'R': 6.41,
            'O': 6.06,
            'D': 5.93,
            'S': 3.73,
            'L': 3.57,
            'G': 3.40,
            'V': 2.85,
            'H': 2.38,
            'K': 2.25,
            'M': 2.21,
            'U': 1.99,
            'B': 1.58,
            'P': 1.57,
            'W': 1.52,
            'J': 1.46,
            'Z': 1.39,
            'C': 1.24,
            'F': 0.81,
            'X': 0.040,
            'Y': 0.035,
            'Q': 0.009
        }

        self.word_list = WordList()
        self.words_per_letter_count = defaultdict(set)
        for word in self.word_list:
            self.words_per_letter_count[len(word)].add(word)
        self.words_per_letter_count[2] = {'in', 'de', 'op', 'en', 'ja', 'ik'}

        self.tonal_msg = '0 11 18 26 0 26 18 20 2 2 4 18 26 8 13 26 7 4 19 26 11 4 21 4 13 26 8 18 27 26 3 0 13 26 18 19 0 0 19 26 0 26 6 4 11 8 9 10 26 0 0 13 26 23 26 15 11 20 18 26 24 26 15 11 20 18 26 25 28 26 22 4 17 10 26 8 18 26 23 27 26 24 26 8 18 26 18 15 4 11 26 4 13 26 25 26 8 18 26 9 4 26 12 14 13 3 26 3 8 2 7 19 26 7 14 20 3 4 13 28'

    def replace_msg(self, letter_dict: {str: str}) -> str:
        msg = self.msg
        for word, letter in letter_dict.items():
            msg = re.sub(r"\b{}\b".format(word), str(letter), msg)
        msg = msg.replace('   ', '\t')
        msg = msg.replace(' ', '')
        msg = msg.replace('\t', ' ')
        return msg

    def search_space(self):
        for space_word in self.words.copy():
            given_dict = {space_word: '_'}
            msg = self.find_dict(given_dict)
            split_msg = msg.split('_')
            max_length = 0
            max_word = 'NOT FOUND'
            for word in split_msg:
                if len(word) > max_length:
                    max_length = len(word)
                    max_word = word
            print(max_length, max_word, space_word)

    def find_dict(self, given_dict: {str: str} = None) -> str:
        def sort_words(word: str) -> int:
            return self.word_histogram[word]

        def sort_letters(letter: str) -> float:
            return self.letter_histogram[letter]

        if not given_dict:
            given_dict = {
                # 'tonko': 'E',
            }
        unused_words = {word for word in self.words if word not in given_dict.keys()}
        unused_letters = {letter for letter in string.ascii_uppercase if
                          letter not in given_dict.values() and self.letter_histogram[letter] > 3}
        # print(len(unused_letters))
        # return

        all_combinations = combinations(unused_letters, 7)
        for c in all_combinations:
            for p in permutations(c):
                given_dict.update({
                    'noll': p[0],
                    'hu': p[1],
                    'tonde': p[2],
                    'tongo': p[3],
                    'de': p[4],
                    'go': p[5],
                    'tonko': p[6]
                    # 'me': p[6],
                    # 'la': p[7]
                })

                unused_words = {word for word in self.words if word not in given_dict.keys()}
                unused_letters = {letter for letter in string.ascii_uppercase if letter not in given_dict.values()}
                sorted_unused_words = sorted(unused_words, key=sort_words)
                sorted_unused_letters = sorted(unused_letters, key=sort_letters)

                letter_dict = dict(zip(sorted_unused_words, sorted_unused_letters))
                letter_dict.update(given_dict)
                msg = self.replace_msg(letter_dict)
                self.correct_start(msg)

    def correct_start(self, msg: str, words_before: [str] = None) -> bool:
        """
        Check if the input message starts with at least two correct words
        """

        if not words_before:
            words_before = []

        # if len(words_before) >= 3:
        if len(msg) < 105:
            print(words_before, msg)
            return True

        msg = msg.lower()
        for word_length in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
            chunk = msg[:word_length]
            if chunk in self.words_per_letter_count[word_length]:
                words_before.append(chunk)
                rest = msg[word_length:]
                return self.correct_start(rest, words_before)
        return False

    def perm_dict(self, raw_dict: {str: str}) -> str:
        for c in combinations(raw_dict.keys(), 2):
            update_in_dict = {c[0]: raw_dict[c[1]], c[1]: raw_dict[c[0]]}
            new_dict = raw_dict.copy()
            new_dict.update(update_in_dict)
            print(self.replace_msg(new_dict))


if __name__ == '__main__':
    nht = NollHuTonde()
    print(nht.word_histogram)
    tonal_dict = {
        'noll': 0,
        'an': 1,
        'de': 2,
        'ti': 3,
        'go': 4,
        'su': 5,
        'by': 6,
        'ra': 7,
        'me': 8,
        'ni': 9,
        'ko': 10,
        'hu': 11,
        'vy': 12,
        'la': 13,
        'po': 14,
        'fy': 15,
        'ton': 16,
        'tonan': 17,
        'tonde': 18,
        'tonti': 19,
        'tongo': 20,
        'tonsu': 21,
        'tonby': 22,
        'tonra': 23,
        'tonme': 24,
        'tonni': 25,
        'tonko': 26,
        'tonhu': 27,
        'tonvy': 28,
        'tonla': 29,
        'tonpo': 30,
        'tonfy': 31
    }
    swedish_dict = dict(zip(range(0, 29), [letter for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ   ']))
    times = ['{}.{}'.format(hour, minute) for hour in ['12', '1', '2', '3', '4'] for minute in
             ['00', '10', '20', '30', '40', '50']]
    clock_dict = dict(zip(times, [letter for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ   ']))
    # clock_dict = {'12.00': 'A', '12.10': 'H', '12.20': 'C', '12.30': 'D', '12.40': 'E', '12.50': 'F',
    #               '1.00': 'G', '1.10': 'B', '1.20': 'I', '1.30': 'J', '1.40': 'K', '1.50': 'L',
    #               '2.00': 'M', '2.10': 'N', '2.20': 'O', '2.30': 'P', '2.40': 'Q', '2.50': 'R',
    #               '3.00': 'S', '3.10': 'T', '3.20': 'U', '3.30': 'V', '3.40': 'W', '3.50': 'X',
    #               '4.00': 'Y', '4.10': 'Z', '4.20': ' ', '4.30': ' ', '4.40': ' '}
    print(clock_dict)
    print(nht.replace_msg(clock_dict))

import string
import sys
from itertools import combinations_with_replacement, permutations, product
from pprint import pprint
from typing import Iterator

from word_list import WordList


def get_word_beginnings(length: int, max_length: int = None) -> {str}:
    if max_length:
        return {word[:length]: word for word in WordList() if len(word) <= max_length}
    else:
        return {word[:length]: word for word in WordList()}


def get_word_endings(length: int, max_length: int = None) -> {str}:
    if max_length:
        return {word[length:]: word for word in WordList() if len(word) <= max_length}
    else:
        return {word[length:]: word for word in WordList()}


letter_to_alphabet_score = {letter: number for number, letter in enumerate(string.ascii_lowercase, start=1)}
letter_to_alphabet_score[' '] = 27
letter_to_en_scrabble_score = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5,
                               'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4,
                               'w': 4, 'x': 8, 'y': 4, 'z': 10}
letter_to_nl_scrabble_score = {'a': 1, 'b': 3, 'c': 5, 'd': 2, 'e': 1, 'f': 4, 'g': 3, 'h': 4, 'i': 1, 'j': 4, 'k': 3,
                               'l': 3, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 2, 's': 2, 't': 2, 'u': 4, 'v': 4,
                               'w': 5, 'x': 8, 'y': 8, 'z': 4}

alphabet_score_to_letter = {number: letter for number, letter in enumerate(string.ascii_lowercase, start=1)}
alphabet_score_to_letter[27] = ' '


def word_to_score(word: str, letter_scores: {str: int} = None) -> int:
    if letter_scores is None:
        letter_scores = letter_to_alphabet_score
    word = word.lower()
    return sum(letter_scores[letter] for letter in word)


def word_to_letter(word: str) -> str:
    score = word_to_score(word)
    score = score % 27 or 27  # Modulo 26 with a start of 1
    return alphabet_score_to_letter[score]


def compare(letter_combination, expected_letter):
    letter = word_to_letter(letter_combination)
    if letter != expected_letter:
        print('\t'.join([letter_combination, letter, expected_letter]))


def possible_letter_combinations(expected_letter: str, length: int):
    result = []
    words = {''.join(permutation)
             for combination in combinations_with_replacement(string.ascii_lowercase + ' ', length)
             for permutation in permutations(combination)}
    for word in sorted(words):
        if word_to_letter(word) == expected_letter:
            result.append(word)
    return result


def get_words(nr_dots, *letters: str) -> Iterator[str]:
    all_combis = []
    for letter in letters:
        all_combis.append(possible_letter_combinations(letter, nr_dots))
    for letters in product(*all_combis):
        word = ''.join(letters)
        yield word


def letter_combi(letters: str, extra_letters_before: str = '', extra_letters_after: str = '', nr_dots: int = 2):
    result = set()
    length = nr_dots * len(letters) + len(extra_letters_before) + len(extra_letters_after)
    constraints = get_word_endings(length)
    for word in get_words(nr_dots, *letters):
        lookup = extra_letters_before + word + extra_letters_after
        if lookup in constraints:
            found_word = constraints[lookup]
            print(found_word)
            result.add(found_word)
    result = sorted(result)
    # pprint(result)
    # print(len(result))
    return result


if __name__ == '__main__':
    for letter in 'rogaasa':
        print(letter_to_alphabet_score[letter])
    # letter_combi('e', extra_letters_before='', extra_letters_after='n', nr_dots=2)
    # letter_combi('r', extra_letters_before='allerw', extra_letters_after='')
    # letter_combi('r', 'w')
    # letter_combi('b')
    # letter_combi('q')
    # letter_combi('s')

    sys.exit()

    compare('all', 'y')
    compare('enz', 's')

    compare('waa', 'y')
    compare('rza', 's')
    compare('l', 'r')

    compare('de', 'i')

    compare('ql', 'c')
    compare('kr', 'c')
    compare('an', 'o')
    compare('d', 'd')

import copy

from utils import clean_word
from word_list import WordList

present_letters = 'abdefghijklmnorstuv'

word_list = set(WordList('dutch_words'))


def get_square():
    square = {key: {} for key in present_letters}
    square['a'] = {'n': 3, 'r': 1, 's': 1}
    square['b'] = {'i': 1}
    square['d'] = {'e': 1, 'i': 2, 'j': 1}
    square['e'] = {'e': 2, 'f': 1, 'i': 1, 'k': 1, 'l': 1, 'n': 3, 'r': 1, 't': 5}
    square['f'] = {'t': 1}
    square['g'] = {'m': 1}
    square['h'] = {'e': 4}
    square['i'] = {'j': 1, 'l': 1, 'n': 2, 't': 1}
    square['j'] = {'e': 1, 'k': 1}
    square['k'] = {'e': 1, 'h': 1, 'n': 1}
    square['l'] = {'a': 2, 'u': 1}
    square['m'] = {'e': 2}
    square['n'] = {'a': 1, 'd': 4, 'g': 1, 'u': 1, 'v': 2}
    square['o'] = {'k': 1, 'o': 1}
    square['r'] = {'b': 1, 'd': 1}
    square['s'] = {'l': 1, 't': 1}
    square['t'] = {'e': 3, 'h': 3, 's': 1, 'v': 1}
    square['u'] = {'i': 1, 'o': 1}
    square['v'] = {'a': 2, 'e': 1}
    return square


def total_number_of_letters():
    sum = 0
    square = get_square()
    for head_letter in present_letters:
        tails = square[head_letter]
        for value in tails.values():
            sum += value
    print(sum)


def print_square(square=None):
    if square is None:
        square = get_square()

    print('  ' + ' '.join(present_letters))
    for letter in present_letters:
        print(letter + ' ' + ' '.join([str(square[letter].get(inner_letter, ' ')) for inner_letter in present_letters]))


def print_letters_of_square(square=None):
    if square is None:
        square = get_square()

    result = []
    for letter in present_letters:
        for key, value in square[letter].items():
            result += ([key] * value)
    result = sorted(result)
    print(''.join(result))


def subsequent_square(string: str, square=None):
    if square is None:
        square = get_square()

    print(string)
    string = clean_word(string, allowed_chars='-')
    for head, tail in zip(string[:-1], string[1:]):
        if head != '-' and tail == '-':
            print('Next letters after {}: {}'.format(head, square[head]))
        if head == '-' or tail == '-':
            continue
        square[head][tail] = square[head][tail] - 1
        if square[head][tail] == 0:
            del square[head][tail]
    if tail and tail != '-':
        print('Next letters after {}: {}'.format(tail, square[tail]))


def next_letters(string: str, square=None) -> {str: int}:
    if square is None:
        square = get_square()

    for head, tail in zip(string[:-1], string[1:]):
        square[head][tail] = square[head][tail] - 1
        if square[head][tail] == 0:
            del square[head][tail]
    return square[tail]


def reverse_subsequent_square(string: str):
    square = get_square()
    reverse_square = {}
    for horizontal_letter in present_letters:
        reverse_square[horizontal_letter] = {}
        for vertical_letter in present_letters:
            try:
                reverse_square[horizontal_letter][vertical_letter] = square[vertical_letter][horizontal_letter]
            except KeyError:
                pass

    string = string[::-1]
    subsequent_square(string, reverse_square)


solutions = []
# words_so_far = ['met', 'een', 'verbinding', 'met', 'het', 'vasteland']
words_so_far = ['met', ]


def length_words_so_far():
    return sum([len(word) for word in words_so_far])


# ander: for word in ['bij', 'bil', 'bit', 'bits', 'dijk', 'ding']:
# for word in ['ander', 'arbiter', 'asla', 'aster', 'dijk', 'deel', 'deen', 'deet', 'ding']:
#     word_list.remove(word)

def iterate_possibilities(string):
    if len(string) > length_words_so_far() + 10 and not judge_string(string, words_so_far):
        return
    letter_dict = next_letters(string)
    if not letter_dict:
        if len(string) == 74 and judge_string(string, words_so_far):
            print(string)
    else:
        for next_letter in letter_dict.keys():
            iterate_possibilities(string + next_letter)


def judge_string(string: str, words_so_far: [str], ends_with_t:bool=True):
    for word in words_so_far:
        string = string[len(word):]

    for word_length in range(28, 2, -1):
        word = string[:word_length]
        if word in word_list:
            found = not ends_with_t or word[-1] == 'n'
            if found:
                print(word)
                word_list.remove(word)
                return True
    return False


if __name__ == '__main__':
    # print(next_letters(''.join(['me'])))
    # print(length_words_so_far())
    # iterate_possibilities(''.join(words_so_far))
    # judge_string('meteenanderefteijekelandilandindjkhengmenuinvetherbitethetsluoknvasthetvard', ['met', 'een'])
    wl = WordList('dutch_words')
    long_words = ['vals', 'zwam']
    for word in wl:
        if len(word) == 24:
            long_words.append(word)
    long_words = sorted(long_words)
    for w in long_words:
        print(w)
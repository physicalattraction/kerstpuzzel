import string
import sys
from collections import Counter

from word_list import WordList


def transpose(sudoku: [str]) -> [str]:
    return [''.join(row[index] for row in sudoku)
            for index in range(9)]


sudoku_str = """. efrcho.
j.mbvek.s
zi.ugy.qn
bka.w.cdy
fxih.luer
pth.o.ng 
on.lxq.jw
c.gdjzb.u
.y pmats."""
sudoku = sudoku_str.split('\n')


def is_correct(sudoku: [str]) -> bool:
    for row in sudoku:
        letters = [letter for letter in row if letter != ' ']
        if len(letters) != len(set(letters)):
            print(f'Row contains {letters}')
            return False
    for row in transpose(sudoku):
        letters = [letter for letter in row if letter != ' ']
        if len(letters) != len(set(letters)):
            print(f'Col contains {letters}')
            return False
    for block_row_index in range(0, 9, 3):
        for block_col_index in range(0, 9, 3):
            letters = [sudoku[block_row_index][block_col_index],
                       sudoku[block_row_index][block_col_index + 1],
                       sudoku[block_row_index][block_col_index + 2],
                       sudoku[block_row_index + 1][block_col_index],
                       sudoku[block_row_index + 1][block_col_index + 1],
                       sudoku[block_row_index + 1][block_col_index + 2],
                       sudoku[block_row_index + 2][block_col_index],
                       sudoku[block_row_index + 2][block_col_index + 1],
                       sudoku[block_row_index + 2][block_col_index + 2]]
            letters = [letter for letter in letters if letter != ' ']
            if len(letters) != len(set(letters)):
                print(f'Block ({block_row_index}, {block_col_index}) contains {letters}')
                return False


def substitute_word(sudoku: [str], word: str) -> [str]:
    result = sudoku.copy()
    for index in range(9):
        result[index] = f'{result[index][:index]}{word[index]}{result[index][index + 1:]}'
    return result


def show(sudoku: [str]):
    print('\n'.join(sudoku) + '\n')


def count_letters():
    counter = Counter(sudoku_str)
    print(counter)
    missing_letters = ''
    for key, value in counter.items():
        if value == 2:
            missing_letters += key
        if value == 1:
            missing_letters += key + key
    print(len(missing_letters))
    print(''.join(sorted(missing_letters)))


if __name__ == '__main__':
    count_letters()
    sys.exit()
    wl = WordList()
    nine_letter_words = [word for word in wl if
                         len(word) == 9 and all(letter in string.ascii_lowercase for letter in word)]
    for word_count, word in enumerate(nine_letter_words, start=1):
        substitute_sudoku = substitute_word(sudoku, word)
        print(f'*** {word_count} / {len(nine_letter_words)} ***')
        if is_correct(substitute_sudoku):
            print(word)
            show(substitute_sudoku)
            break
        show(substitute_sudoku)

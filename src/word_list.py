from collections import defaultdict

import os

from utils import clean_word


class WordList:
    DUTCH_WORDS = 'dutch_words'
    DUTCH_SERIES = 'dutch_series'
    DUTCH_MOVIES = 'dutch_movies'
    DUTCH_BANDS = 'dutch_bands'
    DIED2017 = 'died_2017'

    FILENAMES = {DUTCH_WORDS: 'dutch_words.txt',
                 DUTCH_SERIES: 'dutch_series.txt',
                 DUTCH_BANDS: 'dutch_bands.txt',
                 DUTCH_MOVIES: 'dutch_movies.txt',
                 DIED2017: 'died2017.txt'}

    def __init__(self, word_lists: [str] = None):
        if isinstance(word_lists, str):
            word_lists = [word_lists]

        if word_lists is None:
            word_lists = [self.DUTCH_WORDS]
        self.word_lists = word_lists

        self.words_per_letter_count = defaultdict(set)
        for word in self:
            self.words_per_letter_count[len(word)].add(word)

    def __iter__(self):
        for word_list in self.word_lists:
            filename = self.FILENAMES[word_list]
            with open(os.path.join('..', 'txt', filename), 'r') as f:
                for line in f:
                    yield line.replace('\n', '')

    def clean_original(self, original_name: str, new_name: str, allowed_chars: str):
        with open(os.path.join('..', 'txt', 'originals', original_name), 'r') as f:
            result = []
            for line in f:
                result.append(clean_word(line, allowed_chars))
        if result:
            with open(os.path.join('..', 'txt', new_name), 'w+') as f:
                print('Writing file {}'.format(new_name))
                f.write('\n'.join(result))


def search_acronym(word_list: WordList, acronym: str) -> [str]:
    found_acronyms = []
    for word in word_list:
        split_word = word.split(' ')
        if len(split_word) == len(acronym) and all([split_word[x][0] == acronym[x] for x in range(len(acronym))]):
            found_acronyms.append(word)
    return found_acronyms


if __name__ == '__main__':
    wl = WordList()
    # wl.clean_original('LijstNederlandseBands.txt', 'dutch_bands.txt', allowed_chars=' ')
    # wl.clean_original('Died2017.txt', 'died2017.txt', allowed_chars=' ')

    wl = WordList([WordList.DUTCH_MOVIES])
    print(search_acronym(wl, 'lb'))
    # for word in wl:
    #     split_word = word.split(' ')
    #     if len(split_word) == 2 and split_word[0][0] == 'f' and split_word[1][0] == 'c':
    #         print(word)

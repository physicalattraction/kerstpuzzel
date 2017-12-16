import os

from utils import clean_word


class WordList:
    def __init__(self, word_lists: [str] = None):
        if isinstance(word_lists, str):
            word_lists = [word_lists]

        if word_lists is None:
            word_lists = []
        self.word_lists = word_lists

    def __iter__(self):
        for word_list in self.word_lists:
            with open(self.get_file_name(word_list), 'r') as f:
                for line in f:
                    yield line.replace('\n', '')

    def get_file_name(self, word_list: str) -> str:
        filename = {'dutch_words': 'dutch_words.txt',
                    'dutch_series': 'dutch_series.txt',
                    'dutch_bands': 'dutch_bands.txt'}[word_list]
        return os.path.join('..', 'txt', filename)

    def clean_original(self, original_name:str, new_name:str, allowed_chars:str):
        with open(os.path.join('..', 'txt', 'originals', original_name), 'r') as f:
            result = []
            for line in f:
                result.append(clean_word(line, allowed_chars))
        if result:
            with open(os.path.join('..', 'txt', new_name), 'w+') as f:
                print('Writing file {}'.format(new_name))
                f.write('\n'.join(result))

if __name__ == '__main__':
    wl = WordList()
    wl.clean_original('LijstNederlandseBands.txt', 'dutch_bands.txt', allowed_chars=' ')

    wl = WordList(['dutch_bands'])
    for word in wl:
        print(word)

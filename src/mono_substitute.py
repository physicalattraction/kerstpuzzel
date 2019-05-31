import copy

from word_list import WordList


class MonoSubstitute:
    """
    This class is looking for mono-alphabetic substitutions, based on positions of letters in a word

    Complemtary to keyword substitute, in which also mono-alphabetic substitutions are searched for,
    using specific keywords to create dictionaries
    """

    def __init__(self):
        self.wordlist = set(WordList(WordList.DUTCH_WORDS))

    def mono_substitute_words(self, original_words: [str]):
        good_dicts = []
        for word in original_words:
            candidate_dicts = self.mono_substitute_word(word)
            if not good_dicts:
                good_dicts = candidate_dicts
            else:
                good_dicts = self._union_two_lists_of_dicts(good_dicts, candidate_dicts)
            if not good_dicts:
                print('There is no mono-alphabetic substitute for these words')
                return
            print('There are {} candidate dicts'.format(len(good_dicts)))

    def mono_substitute_word(self, original_word: str) -> [str]:
        original_hashed_positions = self.get_hashed_positions_of_letters(original_word)
        good_words = []
        good_dicts = []
        for word in self.wordlist:
            word_hashed_positions = self.get_hashed_positions_of_letters(word)
            if original_hashed_positions == word_hashed_positions:
                good_words.append(word.upper())
                good_dicts.append(self.letter_dict_from_word_to_word(original_word, word.upper()))
        if len(good_words) > 20:
            postfix = ', ...'
        else:
            postfix = ''
        print('{} {} woorden: {}{}'.format(original_word, len(good_words), ', '.join(good_words[:20]), postfix))
        return good_dicts

    def letter_dict_from_word_to_word(self, original_word: str, mapped_word: str) -> {str: str}:
        return {original_letter: mapped_word[i] for i, original_letter in enumerate(original_word)}

    def get_hashed_positions_of_letters(self, original_word: str) -> [str]:
        letters = set([letter for letter in original_word])
        position_of = dict()
        for match_letter in letters:
            position_of[match_letter] = [str(i) for i, original_letter in enumerate(original_word) if
                                         original_letter == match_letter]
        positions = set([''.join(positions) for positions in position_of.values()])
        return positions

    def _union_two_lists_of_dicts(self, dicts_1: [{str: str}], dicts_2: [{str: str}]) -> [{str: str}]:
        result = []
        for dict_1 in dicts_1:
            keys_1 = set(dict_1.keys())
            for dict_2 in dicts_2:
                keys_2 = set(dict_2.keys())
                if all([dict_1[k] == dict_2[k] for k in keys_1.intersection(keys_2)]):
                    good_dict = copy.deepcopy(dict_1)
                    good_dict.update(dict_2)
                    result.append(good_dict)
        return result


if __name__ == '__main__':
    ms = MonoSubstitute()
    msg = 'FDWJDIIH ENIDLEEK IZRLIXZN PJNEEBLX GYNDEJKE NQILJKED IPCPFDDH HSLICQYK'.split(' ')
    msg = 'RCToAlsM hXkmiMnte tC irOgsMWeNtveASpjulTRBfln wezKertez el 2RaO01ksL7T hZ iOlOvQa sYelt rBlnSYK a k'.split(' ')
    msg = 'RCToAlsM hXkmiMnte tC irOgsMWeNtveASpjulTRBfln wezKertez el 2RaO01ksL7T hZ iOlOvQa sYelt rBlnSYK a k'.split(
        ' ')
    msg = 'EMOE, WOND, BANK, TEAK, ZOET, FIJN, SHOW, CRON, GOED'.split(', ')
    msg = ['ENIGE', 'IQWRI']
    ms.mono_substitute_words(msg)

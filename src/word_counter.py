from word_list import WordList

MAX_NR_OCCURRENCES = 4


class WordCounter:
    def __init__(self):
        self.letter_to_value = {'a': 188461, 'b': 565383, 'd': 696149, 'e': 88447, 'g': 265341, 'h': 796023,
                                'i': 388069, 'l': 164207, 'n': 492621, 'o': 477863, 's': 433589, 't': 300767,
                                'u': 902301}
        self.values = [696318, 994738, 186634, 937474, 818450, 387210, 184092,
                       377231, 999091, 293830, 725605, 893049, 394922, 2 * 188461]
        self.value_to_word = {value: [] for value in self.values}
        self.word_list = WordList([WordList.DUTCH_WORDS])

    def determine_words(self):
        for word in self.word_list:
            if any([letter not in self.letter_to_value.keys() for letter in word]):
                continue
            score = sum([self.letter_to_value[letter] for letter in word])
            value = score % 1000000
            if value in self.values:
                self.value_to_word[value].append(word)

    def determine_letter_combinations(self):
        for i in range(MAX_NR_OCCURRENCES ** len(self.letter_to_value)):
            letters = self._determine_letters(i)
            value = self._calculate_value_for_dict(letters)
            if value in self.values:
                word = self._letter_dict_to_word(letters)
                print(i, letters, value, word)
                self.value_to_word[value].append(word)

    def _determine_letters(self, input: int) -> {str: int}:
        letter_count = []
        for i in range(1, len(self.letter_to_value) + 1):
            count = input % MAX_NR_OCCURRENCES
            letter_count.append(count)
            input -= count
            input = int(input / MAX_NR_OCCURRENCES)

        return {letter: count for letter, count in zip(self.letter_to_value.keys(), letter_count)}

    def _calculate_value_for_word(self, word:str) -> int:
        if any([letter not in self.letter_to_value.keys() for letter in word]):
            return 0
        return sum([self.letter_to_value[letter] for letter in word]) % 1000000

    def _calculate_value_for_dict(self, letters: dict):
        return sum([count * self.letter_to_value[letter] for letter, count in letters.items()]) % 1000000

    def _letter_dict_to_word(self, letters: {str: int}) -> str:
        return ''.join([letter * count for letter, count in letters.items()])


if __name__ == '__main__':
    wc = WordCounter()

    # wc.determine_letter_combinations()
    # for value, words in wc.value_to_word.items():
    #     print('{} - {}'.format(value, words))

    text = 'hebban olla uogala nestas hagunnan hinase hi nda thu uuat unbidan uue nu'
    print(text)
    values = [wc._calculate_value_for_word(word) for word in text.split(' ')]
    for now, given in zip(values, wc.values):
        print(now, given)

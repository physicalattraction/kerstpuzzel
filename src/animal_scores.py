letter_index = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12,
                'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23,
                'x': 24, 'y': 25, 'z': 26}
letter_morse_short = {'a': 1, 'b': 3, 'c': 2, 'd': 2, 'e': 1, 'f': 2, 'g': 1, 'h': 4, 'i': 2, 'j': 1,
                      'k': 1, 'l': 3, 'm': 0, 'n': 1, 'o': 0, 'p': 2, 'q': 1, 'r': 2, 's': 3, 't': 0,
                      'u': 2, 'v': 3, 'w': 1, 'x': 2, 'y': 1, 'z': 2}
letter_morse_long = {'a': 1, 'b': 1, 'c': 2, 'd': 1, 'e': 0, 'f': 1, 'g': 2, 'h': 0, 'i': 0, 'j': 3,
                     'k': 2, 'l': 1, 'm': 2, 'n': 1, 'o': 3, 'p': 2, 'q': 3, 'r': 1, 's': 0, 't': 1,
                     'u': 1, 'v': 1, 'w': 2, 'x': 2, 'y': 3, 'z': 2}


class AnimalScorer:
    def __init__(self):
        print(letter_index)
        self.letter_to_number = letter_morse_short
        self.letter_to_number_2 = letter_morse_long
        self.animals = ['aap', 'beer', 'das', 'giraf', 'hert', 'kameel', 'kangoeroe', 'kip', 'krokodil', 'leeuw',
                        'neushoorn', 'nijlpaard', 'olifant', 'slang', 'tijger', 'wolf', 'zebra', 'zeehond']
        print('{} animals: {}'.format(len(self.animals), self.animals))

    def score_animals(self):
        for animal in self.animals:
            score = self.animal_to_score_simple(animal)
            print('{}: {}'.format(animal, score))

    def animal_to_score_simple(self, animal: str):
        x = sum([self.letter_to_number[letter] for letter in animal])
        y = sum([self.letter_to_number_2[letter] for letter in animal])
        return (x, y)

    def animal_to_score_complex(self, animal: str) -> int:
        score = 0
        letters = set()
        for letter in animal:
            if letter not in letters:
                score += self.letter_to_number[letter]
                letters.add(letter)
            else:
                score -= self.letter_to_number[letter]
        score = score % 26
        return score


if __name__ == '__main__':
    animal_scorer = AnimalScorer()
    animal_scorer.score_animals()

import string

from word_list import WordList


class SentenceMaker:
    def __init__(self):
        original_msg = 'Voor de voet weg moet dit probleemveld worden neergetunneld in een motie, om langs deze ' \
                       'weg in lijn met de afspraken met het cabinet al zwaluwstaartend de pijnpunten snelstens ' \
                       'ten bestens af te concluderen'.lower()
        self.original_letters = self.filter_letters(original_msg)
        print(''.join(self.original_letters))

        self.word_list = WordList()

    def filter_letters(self, msg: str) -> [str]:
        return sorted([letter for letter in msg if letter in string.ascii_lowercase])

    def pop_message(self, msg_to_pop: str, msg_to_pop_from: [str] = None) -> [str]:
        if not msg_to_pop_from:
            msg_to_pop_from = self.original_letters.copy()
        msg_to_pop = self.filter_letters(msg_to_pop)
        for letter in msg_to_pop:
            if letter not in string.ascii_lowercase:
                continue
            try:
                msg_to_pop_from.remove(letter)
            except ValueError as e:
                msg_to_pop = 'Popping too many times the letter {}'.format(letter)
                raise ValueError(msg_to_pop) from e
        print('{}/{}'.format(len(msg_to_pop), len(self.original_letters)))
        print(''.join(msg_to_pop_from))
        return msg_to_pop_from

    def find_long_words(self, words_before: [str] = None, msg: str = None):
        if not msg:
            msg = ''.join(self.original_letters)

        if not words_before:
            words_before = ['kerstpuzzel']
            msg = self.pop_message('kerstpuzzel')
            return self.find_long_words(words_before, msg)

        if len(words_before) >= 4:
            print(words_before)
            return

        for word_length in [15, 16, 17, 18, 19, 20]:
            for word in self.word_list.words_per_letter_count[word_length]:
                if word in words_before:
                    continue
                try:
                    msg = self.pop_message(word, msg_to_pop_from=msg)
                    return self.find_long_words(words_before + [word], msg)
                except ValueError:
                    continue


if __name__ == '__main__':
    maker = SentenceMaker()
    messages = [
        # 'de kerstpuzzel is dit jaar erg interessant, maar niet de ergste ooit',
        # 'de ene kerstpuzzel is de andere niet want dan was het wel weer de ene',
        # 'met de kerstpuzzel in bad is als lopen in de regen: je wordt bij beide nat',
        # 'de kerstpuzzel van achttien torent boven alle andere uit als je alleen uitgaat van die storende feiten',
        # 'de kerstpuzzel die nu voor ons ligt is minstens even beangstigend als die van eerdere jaren, maar wel lollig',
        # 'een jaar geen kerstpuzzel opgelost is een jaar niet geleefd',
        # 'met de beste kerstpuzzel van nederland monopoliseert de aivd de tijd tegen het jaareinde waarin creatieve geesten mogen spelen met letters danwel stomme spellen',
        # 'de aivd weet dondersgoed dat de kerstpuzzel resulteert in productiviteitsverlies in heel nederland',
        # 'de ene non vroeg de andere non: heb jij al gebeden voor de kerstpuzzel? waarop de ander antwoordde met: nog niet, liefste, dat gaan we wel snel',
        'op straten en pleinen in gans nederland staat er maar een ding centraal: de kerstpuzzel',
    ]
    for msg in messages:

        maker.pop_message(msg)
    # maker.find_long_words()

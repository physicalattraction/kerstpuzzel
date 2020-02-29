'''
Created on Dec 14, 2015
'''

from pprint import pprint
import string
import itertools

from DictionaryDbManager import DictionaryManager


class CaesarCode:
    def __init__(self):
        try:
            self.dm = DictionaryManager()
        except:
            print('Go to /Applications/XAMPP')
            print('Run sudo ./xamppfiles/xampp startmysql')

        self.letter_shifts = list()
        one_shift = {'A': 'B',
                     'B': 'C',
                     'C': 'D',
                     'D': 'E',
                     'E': 'F',
                     'F': 'G',
                     'G': 'H',
                     'H': 'I',
                     'I': 'J',
                     'J': 'K',
                     'K': 'L',
                     'L': 'M',
                     'M': 'N',
                     'N': 'O',
                     'O': 'P',
                     'P': 'Q',
                     'Q': 'R',
                     'R': 'S',
                     'S': 'T',
                     'T': 'U',
                     'U': 'V',
                     'V': 'W',
                     'W': 'X',
                     'X': 'Y',
                     'Y': 'Z',
                     'Z': 'A'
                     }
        cur_shift = one_shift.copy()
        for _ in range(26):
            next_shift = cur_shift.copy()
            for k, v in cur_shift.items():
                next_shift[k] = one_shift[v]
            cur_shift = next_shift
            self.letter_shifts.append(cur_shift)

    def make_shifts_01(self):
        shifts = list()
        wwwword_list = ['AANVAARDBAAR',
                        'AANVECHTBAAR',
                        'BANANENVLAAI',
                        'CENTRIFUGAAL',
                        'CENTRIPETAAL',
                        'CENTRIPETAAT',
                        'CONGLOMERAAT',
                        'CONJECTURAAL',
                        'CONTACTDRAAD',
                        'CONTINENTAAL',
                        'CONTUBERNAAL',
                        'DONDERSTRAAL',
                        'EENRODEDRAAD',
                        'EENHANDSZAAG',
                        'EENHEIDSMAAT',
                        'EINDKAPITAAL',
                        'EINDKWARTAAL',
                        'FANTASIENAAM',
                        'GANGSTERBAAS',
                        'GENIESOLDAAT',
                        'HANENGEKRAAI',
                        'HONDSBRUTAAL',
                        'KANTTEKENAAR',
                        'KINDERSCHAAR',
                        'KONINGSKRAAI',
                        'KONINGSZWAAN',
                        'KUNSTIJSBAAN',
                        'KUNSTMINNAAR',
                        'LANDEIGENAAR',
                        'LANDINGSBAAN',
                        'LANDSDIENAAR',
                        'LANTAARNHAAI',
                        'LANTAARNHAAK',
                        'LANTAARNPAAL',
                        'LANTARENPAAL',
                        'LENTEVERMAAK',
                        'LINGERIEZAAK',
                        'LONGITUDIAAL',
                        'MENGAPPARAAT',
                        'MINISTERRAAD',
                        'MONDVOORRAAD',
                        'MONNIKENBAAI',
                        'MONNIKSCHAAP',
                        'NONSENSICAAL',
                        'NONSENSIKAAL',
                        'ONNAVOLGBAAR',
                        'ORNITHOGRAAF',
                        'PANAMAKANAAL',
                        'PENNINGPLAAT',
                        'PONSAPPARAAT',
                        'SINTNICOLAAS',
                        'TENNISLERAAR',
                        'TENONDERGAAN',
                        'TONEELGEBAAR',
                        'VANIEPENDAAL',
                        'VANILLESMAAK',
                        'VENSTERSTAAF',
                        'VENSTERVRAAT',
                        'VINGERSPRAAK',
                        'WANDELSTRAAT',
                        'WANWIJNSMAAK',
                        'WINKELSTRAAT',
                        'ZANGPAPEGAAI',
                        'ZINKCHROMAAT',
                        'ZINKMINERAAL',
                        'ZONRESULTAAT',
                        'HEKSENGELOOF',
                        'KOKELEKONOOT',
                        'TEKENPOTLOOD']
        for word in wwwword_list:
            shift = dict()
            for src_letter, dst_letter in zip('EILXPAYODWWH', word):
                shift[src_letter] = dst_letter
            shifts.append(shift)
        return shifts

    def caesar_code(self, input_text):
        input_text = input_text.upper()
        for letter_shift in self.letter_shifts:
            text = ''.join([letter_shift[x]
                            if x in letter_shift
                            else x.lower() for x in input_text])
            print(text)

    def print_letter_permutations(self, input_text):
        """Print the input text with all possible letter permutations."""
        letters_sorted = self.sort_letters(input_text)
        all_letters = self._sorted_letters_by_frequency()
        for i in range(6, 6 + 1):
            src_letters = letters_sorted[:i]
            dst_letter_max = 26
            dst_letter_permutations = itertools.permutations(all_letters[:dst_letter_max], i)
            for dst_letters in dst_letter_permutations:
                shift = dict(zip(src_letters, dst_letters))
                permutated_text = self._perform_permutation(input_text, shift)
                print(permutated_text)

    def determine_letter_permutation(self, input_text, allow_double_letters):
        """Determine the permutation that results in a valid text"""
        self.input_text = ''.join(x for x in input_text if x in string.ascii_letters or x == ' ')
        self.letters_sorted = self.sort_letters(input_text)
        print(self.letters_sorted)
        self.all_letters = self._sorted_letters_by_frequency()

        letter_shift = dict(zip(self.all_letters, ['.'] * len(self.all_letters)))
        r = self.add_letter_to_letter_shift(letter_shift, index=0,
                                            allow_double_letters=allow_double_letters)

        if r[0]:
            result = dict()
            for k, v in r[0].items():
                if v != '.':
                    result[k] = v
            # print(result)

            output_text = self._perform_permutation(input_text, result)
            print(output_text)

    def add_letter_to_letter_shift(self, letter_shift, index, allow_double_letters):
        for letter_dst in self.all_letters:
            if not allow_double_letters and letter_dst in letter_shift.values():
                continue
            letter_shift[self.letters_sorted[index]] = letter_dst
            text = self._perform_permutation(self.input_text, letter_shift)
            # print(text)
            valid_text = True
            for word in text.split():
                if not self.dm.words_with_pattern(word, exists=True):
                    valid_text = False
                    #                     print('Word {} is invalid'.format(word))
                    break
            if valid_text:
                if index < len(self.letters_sorted) - 1:
                    letter_shift, ready = self.add_letter_to_letter_shift(letter_shift, index + 1,
                                                                          allow_double_letters)
                    if ready:
                        return (letter_shift, True)
                else:
                    return (letter_shift, True)
            else:
                continue

        letter_shift[self.letters_sorted[index]] = '.'
        return (letter_shift, False)

    def count_letters(self, input_text):
        """Return a letter count for an input text."""
        count_dict = {}
        for x in string.ascii_uppercase:
            count_dict[x] = input_text.count(x)
        return count_dict

    def sort_letters(self, input_text):
        letter_count = self.count_letters(input_text)
        letters = list()
        counts = list()
        for k, v in letter_count.items():
            if v > 0:
                letters.append(k)
                counts.append(v)
        letters_sorted = [i[0] for i in sorted(zip(letters, counts),
                                               key=lambda l: l[1], reverse=True)]
        return letters_sorted

    def permute_with_dict(self, input_text: str, permutation_dict: dict):
        output_list = []
        for c in input_text:
            new_c = permutation_dict.get(c) or c
            output_list.append(new_c)
        print(''.join(output_list))

    def _sorted_letters_by_frequency(self):
        '''From https://onzetaal.nl/taaladvies/advies/letterfrequentie-in-het-nederlands'''
        return ['E', 'N', 'A', 'T', 'I', 'R', 'O', 'D', 'S',
                'L', 'G', 'V', 'H', 'K', 'M', 'U', 'B', 'P',
                'W', 'J', 'Z', 'C', 'F', 'X', 'Y', 'Q']

    def _perform_permutation(self, input_text, letter_shift):
        input_text = input_text.upper()
        text = ''.join([letter_shift[x]
                        if x in letter_shift
                        else x.lower() for x in input_text])
        return text


def geography_permutations():
    msg = 'CGTGIGPDGM, DAFAIHJCHNK, DGPKBPOAS ZSS, DIOOIOOIJJI, DQMMLY- GLMCIFE, FASUW-IUAFSG, ' \
          'FGTJMGHSSN, FIVC, GBSXGFTSMSABGFT, HFYX, HGKJGHBUH, IKUJQ VAJPKJ, IMHHQ-RMAQQGFFAS, ' \
          'IMHSFBGFT, LDLZHFS, LUJGHD CHYH, QBQBOGOGHSSN, RHMFSH, RJVSIHSSN, STJHFA, SYNSHSSN, ' \
          'TFONKTP, TVTNTPQ, VBOQJNBGHSSN, VJPQJDHSSN, VLFEPOSBILFE, VUUMBGFT, WHCEL'

    # Empty permutation dict
    permutation_dict = {
        'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd', 'E': 'e', 'F': 'f', 'G': 'g',
        'H': 'h', 'I': 'i', 'J': 'j', 'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n',
        'O': 'o', 'P': 'p', 'Q': 'q', 'R': 'r', 'S': 's', 'T': 't', 'U': 'u',
        'V': 'v', 'W': 'w', 'X': 'x', 'Y': 'y', 'Z': 'z'
    }

    # Islands
    permutation_dict = {
        'A': 'I', 'B': 'L', 'C': 'M', 'D': 'C', 'E': 'e', 'F': 'N', 'G': 'A',
        'H': 'O', 'I': 'G', 'J': 'j', 'K': 'k', 'L': 'l', 'M': 'R', 'N': 'n',
        'O': 'o', 'P': 'S', 'Q': 'T', 'R': 'B', 'S': 'E', 'T': 'D', 'U': 'U',
        'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'y', 'Z': 'z'
    }

    # Waters
    permutation_dict = {
        'A': 'H', 'B': 'I', 'C': 'c', 'D': 'K', 'E': 'e', 'F': 'L', 'G': 'A',
        'H': 'M', 'I': 'N', 'J': 'O', 'K': 'P', 'L': 'l', 'M': 'G', 'N': 'R',
        'O': 'C', 'P': 'S', 'Q': 'T', 'R': 'B', 'S': 'E', 'T': 'D', 'U': 'u',
        'V': 'V', 'W': 'w', 'X': 'x', 'Y': 'Y', 'Z': 'Z'
    }

    # Rivers
    permutation_dict = {
        'A': 'a', 'B': 'K', 'C': 'L', 'D': 'M', 'E': 'G', 'F': 'N', 'G': 'D',
        'H': 'O', 'I': 'I', 'J': 'P', 'K': 'k', 'L': 'A', 'M': 'R', 'N': 'n',
        'O': 'S', 'P': 'T', 'Q': 'U', 'R': 'r', 'S': 'E', 'T': 't', 'U': 'u',
        'V': 'J', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'
    }

    permutation_dict = {
        'A': 'I', 'B': 'G', 'C': 'J', 'D': 'K', 'E': 'e', 'F': 'L', 'G': 'C',
        'H': 'A', 'I': 'M', 'J': 'N', 'K': 'O', 'L': 'P', 'M': 'm', 'N': 'R',
        'O': 'B', 'P': 'S', 'Q': 'T', 'R': 'r', 'S': 'D', 'T': 'E', 'U': 'U',
        'V': 'V', 'W': 'w', 'X': 'x', 'Y': 'Y', 'Z': 'z'
    }

    cc = CaesarCode()
    cc.permute_with_dict(msg, permutation_dict)


if __name__ == '__main__':
    cc = CaesarCode()
    msg = 'NBKEORUUOEUBIOOXALSAEOWPFXUFUEWUAWOOUUDWALKEGUVAMIXEAKGIEHEEQEOTNUVEESDEOEFUAOBUHIUHDOSHESKAJIUNBATPPNKZIEUVBDKEIEXAOQAEHNUIOSTUYVIETCFITUIEOUKLOEWHHTUUEWPOCOOKAEAUWSIBDAEIGWIEARMUNOESOEEOSSODLIF'
    msg = 'VADSEDFRPTWGGWPPJRVEIEGACTWGHRAQPEGIDJEH'
    cc.caesar_code(msg)

'''
Created on Dec 14, 2015
'''

from pprint import pprint
import string
import itertools


class CaesarCode(object):

    def __init__(self):
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

#         common_letters = ['A', 'E', 'I', 'O', 'U']
#         for h in common_letters:
#             for w in common_letters:
#                 if w is not h:
#                     for e in common_letters:
#                         if e is not h and e is not w:
#                             self.letter_shifts.append({'H': h,
#                                                        'W': w,
#                                                        'E': e})

        self.letter_shifts = list()
        self.letter_shifts.append({
                                   'L': 'N',
                                   'W': 'A'
                                   })
        self.letter_shifts = self.make_shifts_01()
    
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
            pprint(text)
            if 'PERMUTATIE' in text:
                pprint(letter_shift)

    def permutations(self, input_text):
        letter_count = self.count_letters(input_text)
        letters = letter_count.keys()
        counts = letter_count.values()
        letters_sorted = [i[0] for i in sorted(zip(letters, counts),
                                               key=lambda l: l[1], reverse=True)]

        all_letters = self._sorted_letters_by_frequency()
        for i in range(6, 6 + 1):
            src_letters = letters_sorted[:i]
            dst_letter_max = 26
            dst_letter_permutations = itertools.permutations(all_letters[:dst_letter_max], i)
            for dst_letters in dst_letter_permutations:
                shift = dict(zip(src_letters, dst_letters))
                permutated_text = self._perform_permutation(input_text, shift)
                print(permutated_text)

    def count_letters(self, input_text):
        count_dict = {}
        for x in string.ascii_uppercase:
            count_dict[x] = input_text.count(x)
        return count_dict

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

if __name__ == '__main__':
    msg = 'GMEM HWODB OE WLZRC EVLHRGMSEV PRA QEEFHUXO, YOKWGHZEPH HGM GSR VHDHYYQXQDTEPREV UCJIDVOQDBL (OWH DYH EILXPAYODWWH), ZDTEXH WWL HHQ SHUPXWDWLH HQ WHQ VORWWH MET CAESAR'
    msg = 'GMEM HWODB OE WLZRC EVLHRGMSEV PRA QEEFHUXO, YOKWGHZEPH HGM GSR VHDHYYQXQDTEPREV UCJIDVOQDBL (OWH DYH EILXPAYODWWH), ZDTEXH WWL'
    msg = '(OWH DYH EILXPAYODWWH), ZDTEXH WWL'
#     msg = 'HWODB QEEFHUXO'
#     msg = 'TPR SYSTRH JL AJGTJQ TEQQ EIA KQJLRSSJQ LRTPRQ'
#     msg = 'REEP, FRIET, PUPPY, BUL, ROS, LOG, GONG, TOORN, LINDE, TEELT'
#     msg = 'KA LOF, COSEN EN PRE; UTS KAAV; T TPTAA ( COMAAL); CF-CATAT ; DT;QUTUTAI; ,WTUK;TTEEEE;VT;KCF;GMTJE'
#     msg = 'HLBDNE IPTKBR FT VEK E KEEP I. VTPITTHSDKB IPTKBR FT LVTPEH.'
#     msg = 'HLBDNE'
    cc = CaesarCode()
    cc.caesar_code(msg)
#     cc.count_letters(msg)
#     cc.permutations(msg)

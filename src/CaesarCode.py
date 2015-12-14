'''
Created on Dec 14, 2015
'''

from pprint import pprint
import string


class CaesarCode(object):

    def __init__(self):
        self.letter_shifts = list()
        self.letter_shifts .append({'A': 'B',
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
                                    })
        common_letters = ['A', 'E', 'I', 'O', 'U', 'N', 'S', 'R', 'T', 'D', 'L']
        common_letters = ['A', 'E', 'O', 'U']
        for h in common_letters:
            for w in common_letters:
                if w is not h:
                    for e in common_letters:
                        if e is not h and e is not w:
                            self.letter_shifts.append({'H': h,
                                                       'W': w,
                                                       'E': e})

    def caesar_code(self, input_text):
        input_text = input_text.upper()
        for letter_shift in self.letter_shifts:
            text = ''.join([letter_shift[x]
                            if x in letter_shift
                            else x.lower() for x in input_text])
            pprint(text)

    def count_letters(self, input_text):
        count_dict = {}
        for x in string.ascii_uppercase:
            count_dict[x] = input_text.count(x)
        pprint(count_dict)

if __name__ == '__main__':
    msg = 'GMEM HWODB OE WLZRC EVLHRGMSEV PRA QEEFHUXO, YOKWGHZEPH HGM GSR VHDHYYQXQDTEPREV UCJIDVOQDBL (OWH DYH EILXPAYODWWH), ZDTEXH WWL HHQ SHUPXWDWLH HQ WHQ VORWWH MET CAESAR'
    cc = CaesarCode()
    cc.caesar_code(msg)
    cc.count_letters(msg)

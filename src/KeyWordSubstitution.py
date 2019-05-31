import string
from collections import OrderedDict

from word_list import WordList


class KeyWordSubstitution:
    def __init__(self):
        self.permutation_dict = OrderedDict()
        self.wordlist = set(WordList(WordList.DUTCH_WORDS))

    def create_permutation_dict(self, keyword: str):
        alphabet = string.ascii_uppercase
        used_letters = set()
        self.permutation_dict = OrderedDict()

        # Add the letters from the keyword
        for letter in keyword:
            letter = letter.upper()
            if letter not in used_letters:
                if letter not in alphabet:
                    continue
                dst_letter = alphabet[len(used_letters)]
                self.permutation_dict[letter] = dst_letter
                used_letters.add(letter)

        # Add all other letters
        for letter in alphabet:
            if letter not in used_letters:
                dst_letter = alphabet[len(used_letters)]
                self.permutation_dict[letter] = dst_letter
                used_letters.add(letter)

        # self._print_permutation_dict()

    def _print_permutation_dict(self):
        print(''.join(list(self.permutation_dict.keys())))
        print(''.join(list(self.permutation_dict.values())))

    def permute_message(self, original_msg:str):
        original_msg = original_msg.upper()
        permuted_letters = []
        for x in original_msg:
            if x in self.permutation_dict:
                permuted_letters.append(self.permutation_dict[x])
            else:
                permuted_letters.append(x)
        # print(original_msg)
        result = ''.join(permuted_letters)
        return result

    def permute_message_useful_word(self, original_msg:str):
        result = self.permute_message(original_msg)
        split_result = result.split(' ')
        if any([word in self.wordlist for word in split_result]):
            print(original_msg)


if __name__ == '__main__':
    kws = KeyWordSubstitution()
    for person in kws.wordlist:
        kws.create_permutation_dict(person)
        # print('\n{}'.format(person))
        msg = 'FDWJDIIH ENIDLEEK IZRLIXZN PJNEEBLX GYNDEJKE NQILJKED IPCPFDDH HSLICQYK'
        kws.permute_message_useful_word(msg)

    # kws.permute_message('NZR NNFVYT QJG IWQN IQFLLNJQ')
    # kws.permute_message('XS UOOH VSH DOG NWSB OZG XS VSH RCCF VSPH')
    # kws.permute_message('ANLNISUEWHTINSJECDNOENRBUEAKNLNHEEBB')
    # kws.permute_message('VROPRIDGIVDLWSEHVANBIVRWRWVAASIGMXCVOVRTQDPWPEECSZAIIROADMECANRT')
    # kws.permute_message('RM ELVGYZO RH SVG HRNKVO: QV YVMG LU LK GRQW LU QV YVMG GV OZZG. ZOH QV GV OZZG YVMG, NLVG QV ALITVM WZG QV LK GRQW EVIGIVPG')
    # kws.permute_message('TMAVFEKUOBOBRNRSEVVALCYAVNMAMASSWETIC')
    # kws.permute_message('PDULAF NAONPG NAIPRY PBEFDP ULDELQ NAPYAP RTGLEL PKWTAR NAPHTO UBDBGC XEABAB GXCNEW BABAGL GXENEW BACAGL GXENEW BABAGL GXCNEW BAEAGL GXBNEW BAEAGL GXCNEW BABAGL GXCNEW BABAGL GXENEW BACAGL GVENEW BABAGL GXBNEW BAEAGL GXBNEW BAEAGL GXENEW BABAGL GXCNEW BABAGL GXENEA NARKLO EDXEAC ABGXAZ')

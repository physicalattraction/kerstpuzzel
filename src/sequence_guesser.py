import string


def modulo_26_as_letter(seq):
    position_to_letter = dict(zip(range(1, 27), [letter for letter in string.ascii_lowercase]))
    positions = [x % 26 + 1 for x in seq]
    letters = [position_to_letter[x] for x in positions]
    print(''.join(letters))


if __name__ == '__main__':
    seq = [2083455, 1066049, 1530205, 1528413, 1529437, 1070657, 2086271, 6144, 1557056, 1838013, 619790, 1455037,
           323024, 7610, 2084366, 1069070, 1531425, 1531892, 1529152, 1065980, 2088234]
    modulo_26_as_letter(seq)

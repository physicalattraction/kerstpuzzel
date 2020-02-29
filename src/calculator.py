import sys
from math import pi


def waarde_van_data():
    for b in range(1, 10):
        for i in range(1, 10):
            digits_used = {b}
            if i in digits_used:
                continue
            i_string = str(i)
            for g in range(1, 10):
                digits_used = {b, i}
                if g in digits_used:
                    continue
                g_string = str(g)
                for d in range(4, 10):
                    digits_used = {b, i, g}
                    if d in digits_used:
                        continue
                    for a in range(1, 10):
                        digits_used = {b, i, g, d}
                        if a in digits_used:
                            continue
                        for t in range(1, 10):
                            digits_used = {b, i, g, d, a}
                            if t in digits_used:
                                continue
                            digits_used = {b, i, g, d, a, t}
                            big = 100 * b + 10 * i + g
                            data = 1000 * d + 100 * a + 10 * t + a
                            big_times_data = big * data
                            bigdata = 10000 * big + data
                            groei = bigdata - big_times_data
                            groei_str = str(groei)
                            if len(groei_str) == 5 and groei_str[0] == g_string and groei_str[4] == i_string \
                                    and '0' not in groei_str[1:4] \
                                and groei_str[1] not in digits_used \
                                and groei_str[2] not in digits_used and groei_str[2] != groei_str[1] \
                                and groei_str[3] not in digits_used:
                                print('*** Found a solution ***')
                                print('BIG', big)
                                print('DATA', data)
                                print('GROEI', groei)
                                print('BIGDATA', bigdata)
                                # sys.exit()


def print_pi():
    pi_string = (f'{pi:.1000000f}')
    print('14' in pi_string)


waarde_van_data()
# print_pi()

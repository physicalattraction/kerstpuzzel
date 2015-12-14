'''
Created on Dec 14, 2015
'''

from CsvReader import CsvReader
import itertools


class CountryQuiz(object):

    def __init__(self):
        self.read_country_info()

    def read_country_info(self):
        csv_reader = CsvReader()
        fields, lines = csv_reader.read_csv(csv_file='kerstpuzzel_landen.csv',
                                            header_present=True)
        countries = csv_reader.transform_csv_structure_into_json_structure(fields, lines)

        self.population = {}
        self.area = {}
        for country in countries:
            self.population[country['Land']] = int(country['Inwoners'])
            self.area[country['Land']] = int(country['Oppervlak'])

    def split_in_two(self):
        for data in [self.population, self.area]:
            total = sum(data.values())
            diff_min = 1e9
            for n in range(1, 9):
                combinations = itertools.combinations(data.keys(), n)
                for cc in combinations:
                    c = [data[x] for x in cc]
                    g1 = int(sum(c))
                    g2 = total - g1
                    diff = abs(g1 - g2)
                    if diff < diff_min:
                        diff_min = diff
                        cc_min = cc
                        g1_min = g1
                        g2_min = g2
            print(cc_min)
            print('Group 1: {}. Group 2: {}. Difference: {}'.
                  format(g1_min, g2_min, diff_min))

if __name__ == '__main__':
    cq = CountryQuiz()
    cq.split_in_two()

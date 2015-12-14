'''
Created on Dec 7, 2015
'''

import csv
from pathlib import Path


class CsvReader(object):
    '''This class is responsible for reading a csv file, returning it in a JSON-like structure.'''

    def __init__(self):
        self.data_dir = Path(__file__).parents[1] / 'csv'
        self.delimiter = ';'
        self.quotechar = '"'

    '''
    Read a csv file and return in same csv structure

    Inputs
    ------
    csv_file : string with the name of the file (not full path)
    header_present : boolean, indicating whether the csv file has a header or not

    Returns
    -------
    fields : list of string with the names of the fields (taken from header).
            If header_present = False, this list is returned empty.
    lines : list of lists of strings, where the outer list represent all lines in the csv file,
            and the inner list represents each field per line.

    Example
    -------
    >>> read_csv('MasterdataVanBommel.csv')
    >>> (['article_property', 'code', 'specification_of', 'name', 'sorting'],
         [['color_group', '0', '', 'zwart', ''],
          ['color_group', '1', '', 'wit', ''],
          ['article_group', '2868', '', 'DAMES SANDAAL RZ BLAUW', ''],
          ['article_group', '2869', '', 'DAMES SANDAAL RZ OVERIGE', ''],
          ['material', 'ANILI', '', 'Aniline', ''],
          ['material', 'ZEBRA', '', 'ZEBRA', '']])
    '''
    def read_csv(self, csv_file, header_present=True):
        fields = list()
        lines = list()

        csv_file_full_path = self.data_dir / csv_file
        with csv_file_full_path.open(mode='r', encoding='utf-8') as file_handle:
            file_reader = csv.reader(file_handle,
                                     delimiter=self.delimiter,
                                     quotechar=self.quotechar)
            header_processed = False
            for line in file_reader:
                if header_present and not header_processed:
                    fields = line
                    header_processed = True
                else:
                    lines.append(line)

        return fields, lines

    '''
    Transform a csv-like Python structure into a json-like Python structure

    Inputs
    ------
    fields : list of string with the names of the fields
    lines : list of lists of strings, where the outer list represent all records,
            and the inner list represents each field per line

    Returns
    -------
    result : nested dictionary

    Example
    -------
    >>> fields, lines = read_csv('MasterdataVanBommel.csv')
    >>> transform_csv_structure_into_json_structure(fields, lines)
    >>> [{'article_property': 'color_group',
          'code': '0',
          'name': 'zwart',
          'sorting': None,
          'specification_of': None},
         {'article_property': 'color_group',
          'code': '1',
          'name': 'wit',
          'sorting': None,
          'specification_of': None},
         {'article_property': 'article_group',
          'code': '2868',
          'name': 'DAMES SANDAAL RZ BLAUW',
          'sorting': None,
          'specification_of': None},
         {'article_property': 'article_group',
          'code': '2869',
          'name': 'DAMES SANDAAL RZ OVERIGE',
          'sorting': None,
          'specification_of': None},
         {'article_property': 'material',
          'code': 'ANILI',
          'name': 'Aniline',
          'sorting': None,
          'specification_of': None},
         {'article_property': 'material',
          'code': 'ZEBRA',
          'name': 'ZEBRA',
          'sorting': None,
          'specification_of': None}]
    '''
    def transform_csv_structure_into_json_structure(self, fields, lines):
        result = list()
        for line in lines:
            # Replace empty strings by None (NULL)
            line = [x if x != '' else None for x in line]
            result.append(dict(zip(fields, line)))
        return result

if __name__ == '__main__':
    cr = CsvReader()

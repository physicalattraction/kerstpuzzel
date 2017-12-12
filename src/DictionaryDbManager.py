"""
Created on Dec 20, 2015
"""

from DB.SqlHelper import SqlHelper
from DB.DBManager import DBManager


class DictionaryManager(object):
    """
    Manage the Dutch dictionary
    """

    def __init__(self):
        config = DBManager.get_config('puzzle')
        self.db = DBManager(config)

    def is_valid_word(self, input_word):
        """Verify if the input text belongs to Dutch language"""
        sql = """SELECT word FROM stripped WHERE word = '{}' LIMIT 1""".format(input_word)
        r = self.db.fetch_as_array(sql, col=0)
        if not r:
            return False
        else:
            return True

    def words_with_pattern(self, input_word, exists=False):
        """
        Return all words with the given pattern.

        Inputs
        ------
        pattern: word with periods as jokers.
        exists: flag indicating whether to check if a word merely has to exist.

        Returns
        -------
        If exists == False: List of words that match the input pattern. Words are capitalized.
        If exists == True: Boolean to indicate if a word with the given input pattern exists.

        Example
        -------
        >>> words_with_pattern('u.tge...en')
        >>> ['UITGEBETEN', 'UITGEBOGEN', 'UITGEGETEN', 'UITGEGETEN', 'UITGEGOTEN',
             'UITGEKOMEN', 'UITGEKOZEN', 'UITGELADEN', 'UITGELOPEN', 'UITGEMALEN',
             'UITGENEPEN', 'UITGEREDEN', 'UITGEREZEN', 'UITGEVAREN', 'UITGEWEKEN',
             'UITGEWEZEN', 'UITGEWOGEN', 'UITGEZETEN', 'UITGEZOGEN', 'UITGEZOPEN']
        """
        selection = dict()
        for i, input_char in enumerate(input_word):
            if input_char != '.':
                field = 'letter{:02d}'.format(i + 1)
                selection[field] = input_char.upper()
        field = 'letter{:02d}'.format(i + 2)
        selection[field] = ''
        selection_sql = SqlHelper.criteria_dict_to_selection_sql(selection)

        sql = 'SELECT word FROM by_letter WHERE {}'.format(selection_sql)

        if exists:
            sql += ' LIMIT 1'
            r = self.db.fetch_as_array(sql)
            if not r:
                return False
            else:
                return True
        else:
            r = self.db.fetch_as_array(sql)
            return r

if __name__ == '__main__':
    dm = DictionaryManager()
    print(dm.is_valid_word('uitgegeten'))
    print(dm.is_valid_word('uitgegeeten'))
    print(dm.is_valid_word('EEN'))
    print(dm.words_with_pattern('u.tge...en'))
    print(dm.words_with_pattern('.E.'))
    print(dm.words_with_pattern('u.tge...en', exists=True))
    print(dm.words_with_pattern('u.tge.ee.en', exists=True))
    print(dm.words_with_pattern('aa.', exists=True))

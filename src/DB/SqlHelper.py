'''
Created on Sep 10, 2015

@author: Erwin Rossen
'''


class SqlHelper(object):
    '''
    This class defines common SQL functionality
    '''

    def __init__(self, fe_db_manager, fe_db_name, fe_article_table_name, fe_id_tenant):
        self.fe_db = fe_db_manager
        self.fe_db_name = fe_db_name
        self.fe_article_table_name = fe_article_table_name
        self.fe_id_tenant = fe_id_tenant

    def select_minimum_value(self, fe_field, criteria):
        """Select the most occuring value of field 'fe_field' that adheres to the criteria."""

        selection_sql = self.criteria_dict_to_selection_sql(criteria)
        q = '''
            SELECT MIN({field})
            FROM {db}.{table}
            WHERE {selection_sql}
        '''.format(field=fe_field, db=self.fe_db_name, table=self.fe_article_table_name,
                   selection_sql=selection_sql)
        field_value = self.fe_db.fetch_as_value(q)
        return field_value

    def select_most_occurring_value(self, fe_field, criteria):
        """Select the most occuring value of field 'fe_field' that adheres to the criteria."""

        selection_sql = self.criteria_dict_to_selection_sql(criteria)
        q = '''
            SELECT {field}, COUNT(fe_identifier) AS count
            FROM {db}.{table}
            WHERE {selection_sql}
            GROUP BY {field}
            ORDER BY count DESC
        '''.format(field=fe_field, db=self.fe_db_name, table=self.fe_article_table_name,
                   selection_sql=selection_sql)
        try:
            field_value = self.fe_db.fetch_as_array_of_arrays(q)[0][0]
        except IndexError:
            print('Failing SQL:\n{}'.format(q))
            raise
        return field_value

    @staticmethod
    def key_value_to_selection_sql(key, value):
        """Transform a key-value pair into an SQL selection clause."""

        if value is None:
            sql = ''' ({key} IS NULL) '''.format(key=key)
        else:
            sql = ''' ({key} = '{value}') '''.format(key=key, value=value)
        return sql

    @staticmethod
    def criteria_dict_to_criteria_sql(criteria_dict):
        """Transform a dict with criteria into a list of SQL statements of these criteria."""

        criteria_sql = list()
        for key, value in criteria_dict.items():
            sql = SqlHelper.key_value_to_selection_sql(key, value)
            criteria_sql.append(sql)
        return criteria_sql

    @staticmethod
    def criteria_dict_to_selection_sql(criteria_dict):
        """Transform a dict with criteria into a SQL selection statement."""

        criteria_sql = SqlHelper.criteria_dict_to_criteria_sql(criteria_dict)
        selection_sql = ' AND '.join(criteria_sql)
        return selection_sql

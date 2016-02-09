"""
Created on 22 jul. 2014

@author: Erwin Rossen
"""

from datetime import date, time
from decimal import Decimal
from pprint import pprint  # @UnusedImport
import sys

import pymysql

from DB.SqlHelper import SqlHelper
from UtilsContainer import Assert
import numpy as np


class DBManager(object):
    """
    Creates and maintains the database.

    The only direct interface between Python and MySQL
    """

    def __init__(self, config=None, database=None, info_mode=True, debug_mode=False):
        if config is None:
            config = {
                'user': 'root',
                'passwd': 'Nyon6966',
                'host': '83.161.215.203',
                'port': 8889
            }
        Assert.py_type(config, dict, 'MySQL configuration')
        assert 'user' in config
        assert 'passwd' in config
        assert 'host' in config
        assert 'port' in config
        self.config = config

        connection_config = {'user': config['user'],
                             'passwd': config['passwd'],
                             'host': config['host'],
                             'port': config['port'], }
        self.cnx = self._connect_to_mysql(connection_config)
        self.cursor = self.cnx.cursor()
        self.debug = debug_mode
        self.info = info_mode
        if database is not None:
            self.connect_to_database(database)
        elif 'default_db' in config and config['default_db'] is not None:
            self.connect_to_database(config['default_db'])
        self.cnx.autocommit(True)

    @staticmethod
    def get_config(predefined_config):
        """Retrieve a predefined config dictionary for DBManager

        Input:
        ------
        predefined_config: string
            Name of the predefined configuration settings. It shall be a recognized predefined configuration,
            otherwise an AssertionError is raised.
            local: Mac server in office in Utrecht
            aws: Aurora AWS RDS

        Returns:
        --------
        config: dict
            Dictionary with DB connection configuration, necessary for the class DBManager.
        """

        Assert.py_type(predefined_config, str, 'predefined config')

        if predefined_config == 'localhost':
            config = {
                'user': 'root',
                'passwd': '',
                'host': '127.0.0.1',
                'port': 3306,
                'default_db': 'orderwriter'
            }
        elif predefined_config == 'puzzle':
            config = {
                'user': 'root',
                'passwd': '',
                'host': '127.0.0.1',
                'port': 3306,
                'default_db': 'puzzle_words'
            }
        elif predefined_config == 'nyon_office':
            config = {
                'user': 'root',
                'passwd': 'Nyon6966',
                'host': '83.161.215.203',
                'port': 8889
            }
        elif predefined_config == 'orderwriter_test':
            config = {
                'user': 'nyon_test',
                'passwd': 'AbLsLKnq6NJjd8a6',
                'host': '213.206.228.254',
                'port': 3306,
                'default_db': 'orderwriter_20150721',
            }
        elif predefined_config == 'orderwriter_live':
            config = {
                'user': 'nyon_live',
                'passwd': 'BjaNWs29sUeNWyZ4',
                'host': '213.206.228.254',
                'port': 3306,
                'default_db': 'orderwriter'
            }
        elif predefined_config == 'aws_au':
            config = {
                'user': 'root',
                'passwd': 'Nyon6966',
                'host': 'aurora.ck67ii8uyuzl.eu-west-1.rds.amazonaws.com',
                'port': 3306
            }
        elif predefined_config == 'aws_ow':
            config = {
                'user': 'OrderWriter',
                'passwd': 'Nyon6966',
                'host': 'orderwriter.crii9g2k1ak3.eu-central-1.rds.amazonaws.com',
                'port': 3306
            }
        else:
            msg = 'Predefined config "{0}" not recognized.'.format(predefined_config)
            raise AssertionError(msg)
        config['config'] = predefined_config
        return config

    ''' Public methods '''

    def connect_to_database(self, db_name):
        self.cnx.select_db(db_name)

    def execute(self, query, params=None):
        if self.debug:
            print (query)
        try:
            self.cursor.execute(query, params)
        except:
            print ('Last query:\n{0}'.format(query))
            raise

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def rollback(self):
        self.cnx.rollback()

    def drop_database(self, db_name, confirm=False):
        """Drop a database if it exists.

        If the database does not exist, nothing happens. The optional flag 'confirm' shall be
        set to True before any action takes place, as a safeguard.
        """

        if confirm:
            self.execute("DROP DATABASE IF EXISTS {0}".format(db_name))
            if self.debug:
                print ('Database {0} dropped'.format(db_name))
        else:
            msg = 'Need confirmation message to drop a database'
            raise AssertionError(msg)

    def copy_database(self, src_db, dst_db):
        """Copy a backup of the current Fashion Exchange database"""

        # Check for forbidden database names
        forbidden_db_names = ['fe', 'orderwriter', 'orderwriter_support', 'orderwriter_test']
        if dst_db in forbidden_db_names:
            msg = 'Database name `{}` cannot be used for a backup'.format(dst_db)
            raise AssertionError(msg)

        # Create an empty database
        self.create_database(dst_db, force_create=True)
        self.use_database(dst_db)

        # Temporarily disable foreign key checks
        sql = '''SET FOREIGN_KEY_CHECKS = 0'''
        self.execute(sql)

        # Fetch all tables
        sql = '''SHOW TABLES FROM {}'''.format(src_db)
        tables = self.fetch_as_array(sql)

        for table in tables:
            src_table = '{}.{}'.format(src_db, table)
            dst_table = '{}.{}'.format(dst_db, table)
            self.copy_table(src_table, dst_table, force_create=True)

            # Enable foreign key checks again
        sql = '''SET FOREIGN_KEY_CHECKS = 1'''
        self.execute(sql)

    def create_database(self, db_name, force_create=False):
        """Create an empty database.

        Parameters
        ----------
        db_name: string
            Name of the to be created database
        force_create: bool
            Flag indicating if a possible existing database with the same
            name shall be overwritten or not. If force_create = False and
            there is already a database with the name db_name, nothing happens.

        Returns
        -------
        None

        Postconditions
        --------------
        Database with the given name exists.
        If force_create=True: database with the given name is empty.
        """

        Assert.py_type(db_name, str, 'db_name')
        Assert.py_type(force_create, bool, 'force_create')

        if force_create:
            self.drop_database(db_name, confirm=True)
        self.cursor.execute("CREATE DATABASE {0} DEFAULT CHARACTER SET 'utf8'".format(db_name))
        if self.info:
            print ('Database {0} created'.format(db_name))

    def current_database(self):
        """Return a string with the current database.

        Parameters
        ----------
        None

        Returns
        -------
        table_exists: bool
            Name of the current database

        Prerequisites
        -------------
        Connection to the MySQL server must have been made.
        """

        q = "SELECT DATABASE()"
        self.execute(q)
        r = self.cursor.fetchone()[0]
        return r

    def use_database(self, db_name):
        """Set a database as currently in use"""

        q = "USE {0}".format(db_name)
        self.execute(q)

    def table_exists(self, table, db_name=None):
        """Return whether the given Table exists in the current database.

        Parameters
        ----------
        table: string
            Name of the table to look up.

        Returns
        -------
        table_exists: bool
            Flag indicating whether the Table `table` exists in the current database.

        Prerequisites
        -------------
        Connection to a database must have been made.
        """

        # TODO: This pattern with temporarily disabling debug information happens more frequently.
        # Is there a way to write this in some sort of with statement? 

        # Temporarily disable debug information
        current_debug_mode = self.debug
        self.debug = False

        # Make the assertions
        Assert.py_type(table, str, 'table')
        assert self.current_database() is not None, 'Connection to a database shall have been made.'

        if db_name is None:
            db_name = self.current_database()
        q = '''
            SELECT COUNT(`TABLE_NAME`)
            FROM `INFORMATION_SCHEMA`.TABLES 
            WHERE `TABLE_SCHEMA` = '{}' 
            AND `TABLE_NAME` = '{}'
        '''.format(db_name, table)

        # Reenable debug information
        self.debug = current_debug_mode

        # Return the outcome
        return bool(self.fetch_as_value(q))

    def column_exists(self, table, column):
        """Return whether the given column exists in the Table.

        Parameters
        ----------
        table: string
            Name of the table to look in.
        table: string
            Name of the column to look for.

        Returns
        -------
        column_exists: bool
            Flag indicating whether the Table `table` contains a column `column`.

        Prerequisites
        -------------
        The Table `table` shall exist.
        """

        Assert.py_type(table, str, 'table')
        Assert.py_type(column, str, 'column')
        assert self.table_exists(table), 'The Table `{0}` shall exist.'.format(table)

        cols = self.show_columns(table)
        return column in cols

    def drop_table(self, table):
        """Drop a table from the database.

        If the table does not exist in the database, nothing happens.

        Parameters
        ----------
        table: string
            Name of the table to drop.

        Returns
        -------
        None
        """

        Assert.py_type(table, str, 'table')

        drop = 'DROP TABLE IF EXISTS {0}'.format(table)
        self.execute(drop)

    def truncate_table(self, table, disable_foreign_key_checks=False):
        """Truncate a table from the database

        Raises an error if the table does not exists

        Parameters
        ----------
        table: string
            Name of the table to truncate.
        disable_foreign_key_checks: boolean
            Flag indicating whether foreign keys shall be checked

        Returns
        -------
        None
        """

        Assert.py_type(table, str, 'table')
        Assert.table_exists(table, self)

        if disable_foreign_key_checks:
            # Temporarily disable foreign key checks
            sql = '''SET FOREIGN_KEY_CHECKS = 0'''
            self.execute(sql)

        truncate = 'TRUNCATE {}'.format(table)
        self.execute(truncate)

        if disable_foreign_key_checks:
            # Reenable foreign key checks
            sql = '''SET FOREIGN_KEY_CHECKS = 1'''
            self.execute(sql)

    def create_table_from_create(self, create_table_query, force_create=False,
                                 temporary=False):
        """Create a table from a create query.

        Execute the create_table_query to create a table. The name of the Table
        to create is assumed to be the third word of the query.

        Parameters
        ----------
        create_table_query: string
            Valid SQL query to create a Table.
        force_create: bool
            Flag indicating whether `table_out` shall be overwritten if it
            already exists. If it shall not be overwritten and does exist yet,
            nothing happens.
        temporary: bool
            Flag indicating whether `table_out` will be a temporary Table.

        Returns
        -------
        :rtype: bool
            Flag indicating whether `table_out` is indeed written to the DB.
            If False, the table already existed and nothing had happened.

        Prerequisites
        -------------
        Connection to a database must have been made.

        Postconditions
        --------------
        Table exists in current database.

        Example
        -------
        Syntax of create_table_query shall look like:
            CREATE TABLE `name` AS ( <select query> );
        or:
            CREATE TABLE `name` (
              `col1` int(11) NOT NULL,
              `col2` date DEFAULT NULL,
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
        or:
            CREATE TABLE `name` LIKE `ref_table`;
        """

        Assert.py_type(create_table_query, str, 'create_table_query')
        Assert.py_type(force_create, bool, 'force_create')
        assert self.current_database() is not None, \
            'Connection to a database shall have been made.'

        table_name = self._table_name_from_create_query(create_table_query, temporary)

        if force_create and self.table_exists(table_name):
            self.drop_table(table_name)
        try:
            self.execute(create_table_query)
            table_created = True
            if self.info:
                print ('Table {} created'.format(table_name))
        except pymysql.err.InternalError:
            print('Last query:\n{0}'.format(create_table_query))
            raise

        return table_created

    def create_table_from_select(self, table_out, select_query, force_create=False):
        """Create a table from a select query.

        Parameters
        ----------
        table_out: string
            Name of the Table to create.
        select_query: string
            Valid SQL query that returns a Table. Example:
            SELECT <fields> FROM <table> WHERE <condition>
        force_create: bool
            Flag indicating whether `table_out` shall be overwritten if it
            already exists. If it shall not be overwritten and does exist yet,
            nothing happens.

        Returns
        -------
        table_created: bool
            Flag indicating whether `table_out` is indeed written to the DB.
            If False, the table already existed and nothing had happened.

        Prerequisites
        -------------
        Connection to a database must have been made.

        Postconditions
        --------------
        Table 'table_out' exists in current database.
        """

        Assert.py_type(table_out, str, 'table_out')
        Assert.py_type(select_query, str, 'select_query')
        Assert.py_type(force_create, bool, 'force_create')
        assert self.current_database() is not None, \
            'Connection to a database must have been made.'

        create_table_query = 'CREATE TABLE {0} AS ({1})'.format(table_out, select_query)
        table_created = self.create_table_from_create(create_table_query, force_create)

        return table_created

    def create_table_like(self, table_ref, table_out, force_create=False):
        """Create an empty Table with columns like another Table.

        Create the Table `table_out` with columns and properties exactly
        as Table `table_ref`, but with no contents.

        Parameters
        ----------
        table_ref: string
            Name of the reference Table to mimic.
        table_out: string
            Name of the Table to create.
        force_create: bool
            Flag indicating whether `table_out` shall be overwritten if it
            already exists. If it shall not be overwritten and does exist yet,
            nothing happens.

        Returns
        -------
        table_created: bool
            Flag indicating whether `table_out` is indeed written to the DB.
            If False, the table already existed and nothing had happened.

        Prerequisites
        -------------
        Connection to a database must have been made.
        Table 'table_ref' exists (in current database if no database is specified).
        """

        Assert.py_type(table_ref, str, 'table_ref')
        Assert.py_type(table_out, str, 'table_out')
        Assert.py_type(force_create, bool, 'force_create')
        assert self.current_database() is not None, \
            'Connection to a database must have been made.'

        if '.' in table_ref:
            i = table_ref.index('.')
            db_name = table_ref[:i]
            table_name = table_ref[i + 1:]
        else:
            db_name = None
            table_name = table_ref
        assert self.table_exists(table_name, db_name), \
            'Table `table_ref` shall exist (in current database if no database is specified).'

        create_table_query = self._show_create(table_ref)
        create_table_query = create_table_query.replace(table_ref, table_out)
        table_created = self.create_table_from_create(create_table_query, force_create)

        return table_created

    def copy_table(self, src_table, dst_table, force_create):
        """Copy an entire table from src to dst"""

        self.create_table_like(src_table, dst_table, force_create)

        sql = '''
            INSERT INTO {}
            SELECT * FROM {}
        '''.format(dst_table, src_table)
        self.execute(sql)

    def fetch_as_value(self, select_query):
        """Execute a select query with a single outcome (1 row, 1 column) and return the value."""

        result_as_array = self.fetch_as_array(select_query)
        result = result_as_array[0]
        return result

    def fetch_as_array(self, select_query, col=None):
        """Execute a select query with a single column and return the outcome as an array.

        The argument col determines which column in the SELECT query is returned as an array.
        If the argument col is None, the first column is returned.
        :rtype : List[str]
        """

        # TODO: Make use of fetch_as_array_of_arrays

        if col is None:
            col = 0
        self.execute(select_query)
        data = self.fetchall()
        try:
            result = [x[col] for x in data]
        except IndexError:
            msg = 'SELECT query must have at least {0} columns'.format(col)
            raise AssertionError(msg)

        return result

    def fetch_as_array_of_arrays(self, select_query):
        """Execute a select query with multiple columns and return the outcome as an array.

        The argument col determines which column in the SELECT query is returned as an array.
        If the argument col is None, the first column is returned.
        """

        self.execute(select_query)
        data = self.fetchall()
        result = [x for x in data]
        return result

    def fetch_as_dict(self, select_query):
        """Execute a select query and return the outcome as a dict."""

        self.execute(select_query)
        data = self.fetchall()
        try:
            result = dict(data)
        except:
            msg = '\n' + select_query + '\n'
            msg += 'SELECT query must have exactly two columns'
            raise AssertionError(msg)

        return result

    def fetch_as_np_matrix(self, select_query, glob2loc_x, glob2loc_y):
        """Execute a select query and return the outcome as an np matrix.

        Parameters
        ----------
        select_query: string
            Valid SQL query that returns three columns from a Table. Example:
                SELECT person_id, article_number, SUM(purchase_weight)
                FROM orders
                GROUP BY person_id, article_number
        glob2loc_x: dict
            Keys: All possible global values for the first column
            Values: Range from 0,...,N where N is the number of items in the dict
        glob2loc_y: dict
            Keys: All possible global values for the second column
            Values: Range from 0,...,N where N is the number of items in the dict

        Returns
        -------
        result: np matrix
            A numpy matrix where the first two columns indicate the row and column index,
            and the third column in the select query indicates the value of the matrix elements.

        Prerequisites
        -------------
        Argument select_query shall select exactly three columns
        Argument glob2loc_x keys shall contain all encountered values in the first column
        Argument glob2loc_y keys shall contain all encountered values in the second column
        Argument glob2loc_x values shall be a continous range from 1,...N
        Argument glob2loc_y values shall be a continous range from 1,...N
        The third column in the select query shall be a number
        """

        Assert.py_type(glob2loc_x, dict, 'glob2loc_x')
        Assert.py_type(glob2loc_y, dict, 'glob2loc_y')
        max_loc_x = max(glob2loc_x.values())
        nr_rows = len(glob2loc_x)
        assert max_loc_x < nr_rows, 'glob2loc_x values shall be a continous range from 1,...N'
        max_loc_y = max(glob2loc_y.values())
        nr_cols = len(glob2loc_y)
        assert max_loc_y < nr_cols, 'glob2loc_y values shall be a continous range from 1,...N'

        self.execute(select_query)
        data = self.fetchall()
        result = np.zeros(shape=[nr_rows, nr_cols])
        for (x, y, val) in data:
            try:
                row = glob2loc_x[x]
            except KeyError:
                msg = 'Global value {0} not found in glob2loc_x'.format(x)
                raise AssertionError(msg)
            try:
                col = glob2loc_y[y]
            except:
                msg = 'Global value {0} not found in glob2loc_y'.format(y)
                raise AssertionError(msg)
            try:
                result[row, col] = val
            except ValueError:
                raise AssertionError('The third column in the select query shall be a number')

        return result

    def fetch_with_dictcursor(self, select_query):
        """Execute a select query using a DictCursor"""

        prev_cursor = self.cursor
        self.cursor = self.cnx.cursor(pymysql.cursors.DictCursor)
        self.execute(select_query)
        r = self.fetchall()
        self.cursor = prev_cursor
        return r

    def insert_into_table(self, table_name, cols, values, update_on_duplicate=True, db_name=None):
        """Insert the values in the columns of the given Table.

        Parameters
        ----------
        table_name: string
            Name of the table to add the records to
        cols: (numpy) array of strings
            List of the columns to fill
        values: (numpy) array of tuples
            List of the values to fill.
        update_on_duplicate: boolean
            Determines what happens if a duplicate key is encountered
            If True: the record is updated (default)
            If False: the insertion is ignored
        db_name: string
            Name of the database in which the table is defined. If no database name is given,
            the current database is used.

        Returns
        -------
        None

        Prerequisites
        -------------
        Connection to a database shall have been made
        Table `table_name` shall exists
        Table `table_name` shall contain all columns in `cols`

        Postconditions
        --------------
        If possible, all records are added to the Table

        Notes
        -----
        Only 1000 records can be added in a single INSERT INTO statement (MySQL restriction)
        This method breaks up the insertion in multiple insertions of a 1000
        when more than 1000 records need to be inserted.
        """
        Assert.py_type(table_name, str, 'table_name')
        if db_name is not None:
            Assert.py_type(db_name, str, 'db_name')
            table_name = db_name + '.' + table_name
        Assert.nonemptylist(cols)
        for col in cols:
            Assert.py_type(col, str, 'Column {0}'.format(col))
        nr_cols = len(cols)
        Assert.nonemptylist(values)
        for val in values:
            Assert.nonemptylist(val, nr_cols)
        assert self.current_database() is not None, \
            'Connection to a database must have been made.'

        # Split up the values in chunks of 1,000
        max_inserts = 1000
        nr_queries = np.ceil(len(values) / max_inserts)
        list_values = np.array_split(values, nr_queries)

        for vals in list_values:
            # Build up the query
            if update_on_duplicate:
                ignore = ''
            else:
                ignore = 'IGNORE '

            q = "INSERT {0}INTO {1}\n".format(ignore, table_name)
            q += "("
            for i_col, col in enumerate(cols):
                q += col
                if i_col < nr_cols - 1:
                    q += ", "
            q += ")\n"
            q += "VALUES\n"
            for i_val, val in enumerate(vals):
                q += "("
                for i_field, field in enumerate(val):
                    # Field with quotes if necessary
                    if field is None:
                        q += "NULL"
                    elif isinstance(field, str):
                        if field.upper() == "NULL":
                            q += "NULL"
                        else:
                            q += "'{0}'".format(field)
                    elif isinstance(field, date) or isinstance(field, time):
                        q += "'{0}'".format(field)
                    elif isinstance(field, Decimal):
                        # TODO: Note! Decimal is converted here to float!
                        # In principle, this should not matter, if you insert it
                        # in the database again, the desired precision is maintained. 
                        q += "{}".format(float(field))
                    elif np.isnan(field):
                        q += "NULL"
                    elif np.isscalar(field):
                        q += "{0}".format(field)
                    else:
                        msg = 'Type {0} not recognized'.format(type(field))
                        raise AssertionError(msg)
                    # Trailing comma
                    if i_field < nr_cols - 1:
                        q += ", "
                q += ")"
                if i_val < len(vals) - 1:
                    q += ","
                q += "\n"
            if update_on_duplicate:
                q += "ON DUPLICATE KEY UPDATE\n"
                for i_col, col in enumerate(cols):
                    q += "{0}=VALUES({0})".format(col)
                    if i_col < nr_cols - 1:
                        q += ",\n"

            # Execute the query
            self.execute(q)

    def checksum_table(self, table):
        """Return the checksum of the given Table.

        Parameters
        ----------
        table: string
            Name of the Table to calculate the checksum of.

        Returns
        -------
        checksum: long int
            Checksum of the Table.

        Prerequisites
        -------------
        Table shall exist (in current database if no database is specified).

        Notes
        -----
        During the checksum operation, the table is locked with a read lock
        for InnoDB and MyISAM.
        """

        Assert.py_type(table, str, 'table')
        msg = 'Table {0} shall exist (in current database if no database is specified).'.format(table)
        assert self.table_exists(table), msg

        q = '''
            CHECKSUM TABLE {0}
        '''.format(table)
        self.execute(q)
        result = self.fetchone()
        return result[1]

    def index_column(self, table, column):
        """Add an index to a specific column in a Table.

        Parameters
        ----------
        table: string
            Name of the Table to index.
        column: string
            Name of the column to index.

        Returns
        -------
        None

        Prerequisites
        -------------
        Table exists (in current database if no database is specified).
        Column exists in Table
        """

        Assert.py_type(table, str, 'table')
        Assert.py_type(column, str, 'column')
        assert self.table_exists(table)

        index_exists = self._index_exists(table, column)
        if not index_exists:
            q = '''
                ALTER TABLE {table}
                ADD INDEX `{col}_idx` (`{col}` ASC)
            '''.format(table=table, col=column)
            self.execute(q)

    def add_foreign_key(self, table_child, table_parent, col_child, col_parent,
                        on_delete='RESTRICT', on_update='RESTRICT'):
        """Add a foreign key to a Table.

        Parameters
        ----------
        """

        params = {'table_child': table_child, 'table_parent': table_parent,
                  'col_child': col_child, 'col_parent': col_parent,
                  'on_delete': on_delete, 'on_update': on_update}
        
        self.index_column(table_parent, col_parent)
        sql = '''
            ALTER TABLE `{table_child}` 
            ADD CONSTRAINT `fk_{table_child}_{table_parent}_{col_child}`
            FOREIGN KEY (`{col_child}`)
            REFERENCES `{table_parent}` (`{col_parent}`)
            ON DELETE {on_delete}
            ON UPDATE {on_update}
        '''.format(**params)
        self.execute(sql)

    def primary_key_column(self, table, column):
        """Add a primary key to a specific column in a Table."""

        alter = '''
            ALTER TABLE {0}
            ADD PRIMARY KEY (`{1}`)
        '''.format(table, column)
        self.execute(alter)

    def set_variable(self, variable, value):
        set_var = '''
            SET @{0}={1}
        '''.format(variable, value)
        self.execute(set_var)

    ''' Queries '''

    def sneak_preview(self, table):
        """Print the first ten rows of the Table to the console."""

        Assert.py_type(table, str, 'Input table')
        assert self.table_exists(table), \
            'Table {0} shall exist in the database'.format(table)

        show = '''
            SELECT * 
            FROM {0}
            LIMIT 10
        '''.format(table)
        self.execute(show)
        print (self.fetchall())

    def count_rows(self, table):
        """Return the number of rows of the given Table.
        :type table: str
        """

        q = "SELECT COUNT(*) FROM {0}".format(table)
        result = self.cursor.fetch_as_value(q)
        assert isinstance(result, int)
        return result

    #     def read_masterdata(self, md_type):
    #         q = '''
    #             SELECT `key`, `value`
    #             FROM masterdata
    #             WHERE `type` = '{0}'
    #         '''.format(md_type)
    #         return self.fetch_as_dict(q)

    def read_masterdata(self, criteria):
        criteria_sql = list()
        for key, value in criteria.items():
            criteria_sql.append(SqlHelper.key_value_to_selection_sql(key, value))
        selection_sql = ' AND '.join(criteria_sql)
        q = '''
            SELECT `code`, `name`
            FROM masterdata
            WHERE ({selection_sql})
        '''.format(selection_sql=selection_sql)
        return self.fetch_as_dict(q)

    def q_col_type(self, table, column):
        """Return the type of a certain column in a certain table.

        Parameters
        ----------
        TODO
        """
        assert self.column_exists(table, column)

        q = '''
            SHOW COLUMNS FROM {0} LIKE '{1}'
        '''.format(table, column)
        self.execute(q)
        result = self.fetch_as_array(q, col=0)
        return result

    def show_columns(self, table, database_name=None):
        """Return a list of column names of the given Table."""

        if database_name is not None:
            db_name = '{}.'.format(database_name)
        else:
            db_name = ''
        q = '''
            SHOW COLUMNS FROM {db}{table}
        '''.format(db=db_name, table=table)
        self.execute(q)
        cols = [x[0] for x in self.fetchall()]
        return cols

    ''' Private methods '''

    @staticmethod
    def _connect_to_mysql(config):
        try:
            cnx = pymysql.connect(**config)
        except pymysql.err.OperationalError:
            msg = "Invalid Input: Wrong hostname, username or password\n"
            msg += "Hostname: {0}\n".format(config['host'])
            msg += "Username: {0}\n".format(config['user'])
            msg += "Password: {0}\n".format(config['passwd'])
            sys.exit(msg)
        return cnx

    def _show_create(self, table):
        """Returns a string that can be used to create the Table.

        This means without content, but with properties like indexes
        """

        q = '''
            SHOW CREATE TABLE {0}
        '''.format(table)
        self.execute(q)
        return self.fetchone()[1]

    @staticmethod
    def _table_name_from_create_query(create_table_query, temporary):
        """Return the table name in a create table query."""
        t = create_table_query.split()
        if temporary:
            return t[3]
        else:
            return t[2]
        
    def _index_exists(self, table_name, col_name, db_name=None):
        if db_name is None:
            db_name = self.current_database()
        q = '''
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
            WHERE index_schema = '{db_name}'
            AND table_name = '{table_name}'
            AND column_name = '{col_name}'
            AND seq_in_index = 1
        '''.format(db_name=db_name, table_name=table_name, col_name=col_name)
        count = self.fetch_as_value(q)
        result = count > 0
        return result

if __name__ == '__main__':
    config = DBManager.get_config('localhost')
    db = DBManager(config)
    db.copy_database(src_db='orderwriter', dst_db='orderwriter_20150708')
    db.copy_database(src_db='orderwriter_support', dst_db='orderwriter_support_20150708')

"""
This module contains assertions that can be used by any other class

Created on 11 jul. 2014

@author: Erwin Rossen
"""

import numpy as np


def py_type(data, python_type, name):
    """Assert that the type of data is the correct type."""
    msg = '{0} shall be a {1} (is now a {2})'.format(name, python_type, type(data))
    assert isinstance(data, python_type), msg


def posint(data):
    """Assert that the given number is a positive integer."""
    assert isinstance(data, int) or isinstance(data, np.integer), \
        'number ({0}) shall be a non-negative integer'.format(data)
    assert data > 0, 'number shall be a positive integer'


def nonnegint(data):
    """Assert that the given number is a non-negative integer."""
    assert isinstance(data, int) or isinstance(data, np.integer), \
        'number ({0}) shall be a non-negative integer'.format(data)
    assert data >= 0, 'number ({0}) shall be a non-negative integer'.format(data)


def nonneg(data):
    """Assert that the given number is a non-negative number."""
    assert data >= 0, 'number shall be a non-negative integer'


def nonemptylist(data, lst=None):
    """Assert that the given data is a non-empty list."""
    msg = 'data shall be a non-empty list. Current type: {0}'.format(type(data))
    try:
        len_data = len(data)
    except TypeError:
        raise AssertionError(msg)
    if lst is None:
        assert len_data > 0, 'data shall be a non-empty list'
    else:
        assert len_data == lst, 'data shall have {0} elements, now has {1}'.format(lst, len_data)


def nonemptystring(data):
    """Assert that the given input is a non-empty string."""
    py_type(data, str, 'data')
    assert data != '', 'data shall not be an empty string'


def seq(data):
    """Assert that the given data is either a list, a tuple or a numpy ndarray."""
    msg = 'data shall either be a list or a numpy ndarray (type = {0})'.format(type(data))
    assert (isinstance(data, list) or
            isinstance(data, np.ndarray) or
            isinstance(data, tuple)), msg


def npint(data):
    """Assert that the given data is a numpy array with ints."""
    assert isinstance(data, np.ndarray), 'Data shall be a numpy array with ints'
    assert data.dtype == int, 'Data shall be a numpy array with ints'


def datestring(date):
    """Assert that the given data is a string in the format yyyy-mm-dd."""
    py_type(date, str, 'date')
    msg = '{} is not a valid datestring (yyyy-mm-dd)'.format(date)
    assert date[4] == '-', msg
    assert date[6] == '-', msg


def frequency_count(f_count):
    """Assert that a given frequency count is a proper frequency count.

    A frequency count is a list of tuples or a list of lists, in which the first
    element is the property, and the second element is the count.
    """
    nonemptylist(f_count)
    for fc in f_count:
        nonemptylist(fc, 2)


def table_exists(table, db_manager, cols=None):
    """Assert that a given Table exists.

    Parameters:
    -----------
    table: string
        Name of the Table to check for.
    db_manager: DBManager
        Object to communicate with the Database.
    cols: list of strings
        Columns that must be present in the Table.
        If cols = None, this assertion will not be made.
        Optional. Default: cols=None
    """

    # Temporarily disable debug information
    current_debug_mode = db_manager.debug
    db_manager.debug = False

    # Make the assertion
    py_type(table, str, 'Table')
    assert db_manager.table_exists(table), \
        'Table {0} shall exist in the database.'.format(table)
    if cols is not None:
        for col in cols:
            column_exists(table, col, db_manager)

    # Reenable debug information
    db_manager.debug = current_debug_mode


def column_exists(table, column, db_manager):
    """Assert that a given Table contains a certain column.

    Parameters:
    -----------
    table: string
        Name of the Table to check in.
    table: string
        Name of the column to check for.
    db_manager: DBManager
        Object to communicate with the Database.
    """

    # Temporarily disable debug information
    current_debug_mode = db_manager.debug
    db_manager.debug = False

    # Make the assertion
    py_type(table, str, 'Table')
    assert db_manager.column_exists(table, column), \
        'Table {0} shall contain the column {1}.'.format(table, column)

    # Reenable debug information
    db_manager.debug = current_debug_mode

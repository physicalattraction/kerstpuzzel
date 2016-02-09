"""
Created on 1 jul. 2014

@author: Erwin Rossen
@brief: Public utility functions
"""
import hashlib
import itertools
import operator
import os.path
import random
import string

from UtilsContainer import Assert
import numpy as np


class Switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


''' String operations '''


def remove_non_ascii_chars(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


def random_string(nr_chars=32):
    characters = string.ascii_letters + string.digits
    rs = "".join(random.choice(characters) for _ in range(nr_chars))
    return rs


def generate_identifier(list_of_values, hashed=True):
    # Convert all values to strings
    list_of_strings = list()
    for val in list_of_values:
        list_of_strings.append(str(val))
    # Concatenate
    source_identifier = '_'.join(list_of_strings)
    if hashed:
        return md5(source_identifier)
    else:
        return source_identifier


def read_european_number(european_number):
    """Transform a European number into a float."""
    try:
        number = european_number.replace('.', '')
        number = number.replace(',', '.')
        number = float(number)
        return number
    except ValueError:
        # If the string cannot be converted (e.g. an empty string), the original is returned
        return european_number


def md5(source_string):
    encoded_string = source_string.encode(encoding='utf_8', errors='strict')
    hashed_string = hashlib.md5(encoded_string)
    result = hashed_string.hexdigest()
    return result


def remove_hex_chars(line):
    """Remove all non-printable characters from a string (list of words)."""

    line_after = map(_remove_hex_chars_from_field, line)
    return line_after


def substring_before_character(input_string, character, include_character=False, occurrence='FIRST'):
    """Return the substring before a certain character. Return None if the character does not occur."""
    if occurrence == 'FIRST':
        k = input_string.find(character)
    elif occurrence == 'LAST':
        k = input_string.rfind(character)
    else:
        msg = 'Occurrence {} not recognized. Shall be "FIRST" or "LAST"'.format(occurrence)
        raise AssertionError(msg)
    if k == -1:
        return None
    if include_character:
        k += 1
    new_string = input_string[:k]
    return new_string


def substring_after_character(input_string, character, include_character=False, occurrence='FIRST'):
    """Return the substring after a certain character. Return None if the character does not occur."""
    if occurrence == 'FIRST':
        k = input_string.find(character)
    elif occurrence == 'LAST':
        k = input_string.rfind(character)
    else:
        msg = 'Occurrence {} not recognized. Shall be "FIRST" or "LAST"'.format(occurrence)
        raise AssertionError(msg)
    if k == -1:
        return None
    if not include_character:
        k += 1
    new_string = input_string[k:]
    return new_string


''' List operations '''


def list2dict(lst):
    """
    Convert a list to a dictionary, where the key of each entry are the list
    elements, and the values are indices 0..N, where the ordering is the ordering
    used in the list.
    """

    Assert.seq(lst)

    nr_elements = len(lst)
    result = dict(zip(lst, range(nr_elements)))

    assert isinstance(result, dict), 'Output shall be a dictionary'
    msg = 'All elements of input list ({}) shall be in dictionary ({})'.format(len(result), len(lst))
    assert len(result) == len(lst), msg
    return result

def list2string(lst, separator=" | "):
    """Concatenate all string values in a list.
    
    Empty strings are left out
        """
    
    lst = remove_none_from_list(lst)
    lst = [str(x) for x in lst if x != '']
    return separator.join(lst)


def remove_none_from_list(lst):
    """Filter out all None values from a list."""
    
    return list(filter(None.__ne__, lst))


def reverse_dict(dct):
    """Reverse the dictionaty D: keys will be values, values will be keys."""
    nr_unique_values = len(set(dct.values()))
    msg = 'Dictionary does not have a one-to-one relationship'
    assert nr_unique_values == len(dct), msg
    return {dct[k]: k for k in dct}


def most_common(lst):
    """
    Return the most common element in a list.
    In case of a draw, the element that appears first in the list is selected.
    """

    try:
        # Get an iterable of (item, iterable) pairs
        sorted_list = sorted((x, i) for i, x in enumerate(lst))
        groups = itertools.groupby(sorted_list, key=operator.itemgetter(0))

        # Auxiliary function to get "quality" for an item
        def _auxfun(g):
            _, iterable = g
            count = 0
            min_index = len(lst)
            for _, where in iterable:
                count += 1
                min_index = min(min_index, where)
            return count, -min_index

        # Pick the highest-count/earliest item
        return max(groups, key=_auxfun)[0]
    except TypeError:
        msg = 'Input to most_common shall be an iterable.\n'
        msg += 'Type of L: {0}\n'.format(type(lst))
        raise AssertionError(msg)


def unique(lst):
    """
    Given a seq (any iterable object), return the seq with duplicates removed.
    The order of the elements is unchanged.
    """

    try:
        seen = set()
        seen_add = seen.add
        result = [x for x in lst if not (x in seen or seen_add(x))]
        assert len(result) <= len(lst), 'No elements shall be added'
        return result
    except TypeError:
        msg = 'Input to unique shall be an iterable.\n'
        msg += 'Type of L: {0}\n'.format(type(lst))
        raise AssertionError(msg)


def sort_list_by_another_list(lst_a, lst_b, reverse=False):
    """
    Sort the items in list L by key the items of list M.
    """

    try:
        assert len(lst_a) == len(lst_b), 'Lists L and M shall have equal length'
        result = [x[0] for x in sorted(zip(lst_a, lst_b),
                                       key=operator.itemgetter(1),
                                       reverse=reverse)]
        return result
    except TypeError:
        msg = 'Both inputs to sort_list_by_another_list shall be an iterable.\n'
        msg += 'Type of L: {0}\n'.format(type(lst_a))
        msg += 'Type of M: {0}\n'.format(type(lst_b))
        raise AssertionError(msg)


def filter_array(lst):
    """
    Filter out NaN values from a list or np.array.

    If the type of the input list implements np.isnan, filter out NaN.
    Otherwise, leave the input list unaltered.

    Example
    -------
    >> L = [1, 2, 3, np.nan]
    >> UtilsContainer.filter_array(L)
    [1, 2, 3]
    >> L = np.array(['a', 'b', 'c', np.nan])
    >> UtilsContainer.filter_array(L)
    ['a', 'b', 'c', np.nan]
    """

    Assert.seq(lst)

    try:
        lst_invalid = np.isnan(lst)
    except TypeError:
        lst_invalid = np.zeros_like(lst, dtype=bool)
    lst_valid = np.logical_not(lst_invalid)

    if isinstance(lst, list):
        result = list(lst[i] for i in range(len(lst_valid)) if lst_valid[i])
    elif isinstance(lst, np.ndarray):
        result = lst[lst_valid]
    else:
        msg = 'Input shall be either list or numpy array, is now a {}'.format(type(lst))
        raise AssertionError(msg)

    assert type(lst) == type(result)
    return result


def flatten_np_array(lst):
    """Return an np.array with all elements from all sublists in a list or np.array.

    Note: this does not work for nested sublists!

    Returns
    -------
    flat_array: np.array

    Example
    -------
    >> L = np.array([ [1], [2, 3, 4], [], [2, 3, 4] ])
    >> UtilsContainer.flatten_np_array(L)
    [1  2  3  4  2  3  4]
    """

    flat_array = np.array([a for x in lst for a in (x if isinstance(x, list) else [x])])
    return flat_array


def increment_smallest(lst, dx):
    """Increment the smallest element of the list L with the given amount dx.

    If the minimum occurs multiple times, the first element is incremented."""

    Assert.py_type(lst, np.ndarray, 'L')

    min_index = np.argmin(lst)
    lst[min_index] += dx


def frequency_count2occurrence_list(frequency_count):
    """Transform a frequency count into an occurrence list.

    A frequency count is a list of tuples or a list of lists, in which the first
    element is the property, and the second element is the count. An occurrence
    list is a list with each property <count> times in it.

    Parameters
    ----------
    frequency_count: list of lists or tuples with length 2

    Returns
    -------
    occurrence_list: np.array, dtype = <type(most general key in frequency_count)>

    Example
    -------
    >> a = [ [0, 4], [1, 2], [2, 3], [10, 1] ]
    >> UtilsContainer.frequency_count2occurrence_list(a)
    [ 0  0  0  0  1  1  2  2  2 10]
    >> a = [ ['a', 4], ['b', 2], ['c', 3], ['d', 1] ]
    >> UtilsContainer.frequency_count2occurrence_list(a)
    ['a' 'a' 'a' 'a' 'b' 'b' 'c' 'c' 'c' 'd']
    """

    Assert.frequency_count(frequency_count)

    occurrence_list = np.empty(0)
    for k, v in frequency_count:
        if k is not None:
            k_list = np.empty(v, dtype=type(k))
            k_list.fill(k)
            occurrence_list = np.append(occurrence_list, k_list)

    return occurrence_list


def filter_none_from_frequency_count(frequency_count):
    """
    Filter out None rows from a frequency count.

    A frequency count is a list of tuples or a list of lists, in which the first
    element is the property, and the second element is the count.

    Parameters
    ----------
    frequency_count: list of lists or tuples with length 2

    Returns
    -------
    new_frequency_count: list of lists or tuples with length 2

    Example
    -------
    >> a = [ [None, 4], [1, 2], [2, 3], [10, 1] ]
    >> UtilsContainer.filter_none_from_frequency_count(a)
    [ [1, 2], [2, 3], [10, 1] ]
    >> a = [ [None, 4], ['None', 2], ['c', 3], ['d', 1] ]
    >> UtilsContainer.filter_none_from_frequency_count(a)
    [ ['None', 2], ['c', 3], ['d', 1] ]
    """

    Assert.frequency_count(frequency_count)

    new_frequency_count = [x for x in frequency_count if x[0] is not None]
    return new_frequency_count


''' Print operations '''


def print_progress(i, nr_steps, print_per_percentage=1):
    """Print to screen the progress whenever the percentage passes an integer"""

    j = (i - 1) / nr_steps * (100 / print_per_percentage)
    k = i / nr_steps * 100 / print_per_percentage
    if int(k) > int(j):
        print ('Progress: {0} out of {1} complete ({2:d}%)'.format(i, nr_steps, round(k * print_per_percentage)))
    elif i == nr_steps:
        print ('Progress: {0} out of {1} complete (100%)'.format(i, nr_steps))


''' Clustering specific operations '''


def normalize_overlap_matrix(mtrx):
    """
    Normalizes a numpy matrix used for overlap matrices,
    by dividing every element A_ij by sqrt(A_ii)*sqrt(A_jj)
    """
    assert isinstance(mtrx, np.ndarray), 'Input shall be a numpy array'
    assert np.isreal(mtrx).all(), 'Numpy array shall contain real numbers'
    assert mtrx.shape[0] == mtrx.shape[1], 'Overlap matrix shall be square'
    assert (np.diag(mtrx) != 0).all(), 'Overlap matrix shall not have 0 on its diagonal'

    b = np.sqrt(np.diag(mtrx))
    result = ((mtrx / b).T / b).T

    return result


''' Color operations '''


def hsb2rgb(hsb):
    """
        Transforms a hsb array to the corresponding rgb tuple
        In: hsb = array of three ints (h between 0 and 360, s and v between 0 and 100)
        Out: rgb = array of three ints (between 0 and 255)
        """
    hsb_h = float(hsb[0] / 360.0)
    hsb_s = float(hsb[1] / 100.0)
    hsb_b = float(hsb[2] / 100.0)

    if hsb_s == 0:
        rgb_r = int(round(hsb_b * 255))
        rgb_g = int(round(hsb_b * 255))
        rgb_b = int(round(hsb_b * 255))
    else:
        var_h = hsb_h * 6
        if var_h == 6:
            var_h = 0  # H must be < 1
        var_i = int(var_h)
        var_1 = hsb_b * (1 - hsb_s)
        var_2 = hsb_b * (1 - hsb_s * (var_h - var_i))
        var_3 = hsb_b * (1 - hsb_s * (1 - (var_h - var_i)))

        if var_i == 0:
            var_r = hsb_b
            var_g = var_3
            var_b = var_1
        elif var_i == 1:
            var_r = var_2
            var_g = hsb_b
            var_b = var_1
        elif var_i == 2:
            var_r = var_1
            var_g = hsb_b
            var_b = var_3
        elif var_i == 3:
            var_r = var_1
            var_g = var_2
            var_b = hsb_b
        elif var_i == 4:
            var_r = var_3
            var_g = var_1
            var_b = hsb_b
        else:
            var_r = hsb_b
            var_g = var_1
            var_b = var_2

        rgb_r = int(round(var_r * 255))
        rgb_g = int(round(var_g * 255))
        rgb_b = int(round(var_b * 255))

    return [rgb_r, rgb_g, rgb_b]


def color2hex(h, s, b):
    """Transform a hsb color into a hex string representing that color."""
    (r, g, b) = hsb2rgb([h, s, b])
    color = '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)
    return color


''' File operations '''


def get_src_dir():
    src_dir = os.path.join(os.path.dirname(__file__), '..')
    _ensure_dir_exists(src_dir)
    return src_dir


def get_config_dir():
    src_dir = get_src_dir()
    config_dir = os.path.join(src_dir, '..', 'config')
    _ensure_dir_exists(config_dir)
    return config_dir


def get_img_dir():
    src_dir = get_src_dir()
    img_dir = os.path.join(src_dir, '..', 'img')
    _ensure_dir_exists(img_dir)
    return img_dir


def get_profile_dir():
    src_dir = get_src_dir()
    profile_dir = os.path.join(src_dir, '..', 'profile')
    _ensure_dir_exists(profile_dir)
    return profile_dir


def _ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory, mode=0o777)


def clean_csv_file(file_name_in, file_name_out):
    patterns = dict()
    #     patterns['\"\"'] = '\"'
    patterns['\\\"'] = ''
    with open(file_name_in, 'r') as f:
        lines = f.readlines()
        with open(file_name_out, 'w') as g:
            for line in lines:
                for pattern, subs in patterns.items():
                    if pattern in line:
                        line = line.replace(pattern, subs)
                g.write(line)


def cat(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            print (line)


def grep(pattern, file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if pattern in line:
                print (line)


def head(lines, file_name):
    i_line = 0
    with open(file_name, 'r') as f:
        while i_line < lines:
            line = f.readline()
            print (line)
            i_line += 1


''' Helper functions for Util functions '''


def _remove_hex_chars_from_field(field):
    unprintable_chars = (char for char in field if char not in string.printable)
    for character in unprintable_chars:
        field = field.replace(character, "")
    return field


if __name__ == '__main__':
    print (substring_after_character('ABC-DEF-GHI', '-', True))
    print (substring_after_character('ABC-DEF-GHI', '-', True, 'LAST'))
    print (substring_after_character('ABC-DEF-GHI', '-', False, 'LAST'))

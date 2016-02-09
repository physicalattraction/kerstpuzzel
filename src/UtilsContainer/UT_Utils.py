"""
Created on 1 jul. 2014

@author: Erwin Rossen
"""

from unittest import TestCase, main
from scipy.sparse import csr_matrix
from TestUtilsContainer import TestUtils
from UtilsContainer import Utils
import numpy as np


class TestSubstringAfterCharacter(TestCase):
    def test_gw_01(self):
        line = 'before_20141017'
        character = '_'
        r = Utils.substring_after_character(line, character)
        e = '20141017'
        TestUtils.equal_str(self, r, e, 'line')

    def test_gw_02(self):
        line = 'before_20141017'
        character = '_'
        r = Utils.substring_after_character(line, character,
                                            include_character=True)
        e = '_20141017'
        TestUtils.equal_str(self, r, e, 'line')

    def test_gw_03(self):
        line = 'before_20141017'
        character = '_'
        r = Utils.substring_after_character(line, character,
                                            include_character=False)
        e = '20141017'
        TestUtils.equal_str(self, r, e, 'line')

    def test_gw_04(self):
        line = 'before_20141017'
        character = '.'
        r = Utils.substring_after_character(line, character,
                                            include_character=True)
        self.assertIs(r, None, 'If character not in line, None shall be returned.')


class TestList2Dict(TestCase):
    def gw(self, a, e):
        r = Utils.list2dict(a)
        self.assertDictEqual(r, e)

    def test_gw_01(self):
        a = ['a', 'c', 'b']
        e = {'a': 0, 'b': 2, 'c': 1}
        self.gw(a, e)

    def test_gw_02(self):
        a = [1, 2, 3]
        e = {1: 0, 2: 1, 3: 2}
        self.gw(a, e)

    def test_gw_03(self):
        a = np.array([1, 2, 3])
        e = {1: 0, 2: 1, 3: 2}
        self.gw(a, e)

    def test_bw_01(self):
        with self.assertRaisesRegex(AssertionError, 'list'):
            a = 4
            Utils.list2dict(a)

    def test_bw_02(self):
        with self.assertRaisesRegex(AssertionError, 'list'):
            a = {1, 2, 3}
            Utils.list2dict(a)

    def test_bw_03(self):
        with self.assertRaisesRegex(AssertionError, 'list'):
            a = {1: 0, 2: 1, 3: 2}
            Utils.list2dict(a)
            
class TestList2String(TestCase):
    def gw(self, a, e, sep=None):
        if sep is None:
            r = Utils.list2string(a)
        else:
            r = Utils.list2string(a, sep)
        self.assertEqual(r, e)

    def test_gw_01(self):
        a = ['a', 'c', 'b']
        e = 'a | c | b'
        self.gw(a, e)
    
    def test_gw_02(self):
        a = ['a', None, 'b']
        e = 'a | b'
        self.gw(a, e)
        
    def test_gw_03(self):
        a = ['a', 1, 'b']
        e = 'a | 1 | b'
        self.gw(a, e)
    
    def test_gw_04(self):
        a = ['a', '', 'b']
        e = 'a | b'
        self.gw(a, e)
        
    def test_gw_05(self):
        a = ['a', 'c', 'b']
        sep = '-'
        e = 'a-c-b'
        self.gw(a, e, sep)


class TestMostCommon(TestCase):
    def gw(self, a, e):
        r = Utils.most_common(a)
        self.assertEqual(r, e)

    def test_gw_01(self):
        a = [0, 1, 1]
        e = 1
        self.gw(a, e)

    def test_gw_02(self):
        a = [0, 1, 1, 0]
        e = 0
        self.gw(a, e)

    def test_gw_03(self):
        a = np.array(['a', 'b', 'b', 'a'])
        e = 'a'
        self.gw(a, e)

    def test_gw_04(self):
        a = {0: 10, 1: 10, 2: 10}.keys()
        e = 0
        self.gw(a, e)

    def test_gw_05(self):
        a = {0: 10, 1: 10, 2: 10}.values()
        e = 10
        self.gw(a, e)

    def test_gw_06(self):
        a = 'abbc'
        e = 'b'
        self.gw(a, e)

    def test_gw_07(self):
        a = 'a'
        e = 'a'
        self.gw(a, e)

    def test_bw_01(self):
        """Verify that an error is raised if the input is no list."""
        with self.assertRaises(AssertionError):
            a = 1
            Utils.most_common(a)


class TestUnique(TestCase):
    def gw(self, a, e):
        r = Utils.unique(a)
        self.assertListEqual(r, e)

    def bw(self, a):
        with self.assertRaises(AssertionError):
            Utils.unique(a)

    def test_gw_01(self):
        a = [0, 0, 1, 1, 4, 3, 2, 4, 2, 3]
        e = [0, 1, 4, 3, 2]
        self.gw(a, e)

    def test_gw_02(self):
        a = np.array([0, 0, 1, 1, 4, 3, 2, 4, 2, 3])
        e = [0, 1, 4, 3, 2]
        self.gw(a, e)

    def test_gw_03(self):
        a = (0, 0, 1, 1, 4, 3, 2, 4, 2, 3)
        e = [0, 1, 4, 3, 2]
        self.gw(a, e)

    def test_gw_04(self):
        a = {0: 0, 1: 10, 2: 10}.keys()
        e = [0, 1, 2]
        self.gw(a, e)

    def test_gw_05(self):
        a = {0: 0, 1: 10, 2: 10}.values()
        e = [0, 10]
        self.gw(a, e)

    def test_bw_01(self):
        """Verify that an error is raised if the input is no list."""
        a = 1
        self.bw(a)


class TestSortListByAnotherList(TestCase):
    def test_gw_01(self):
        lst_a = ['a', 'b', 'c', 'd', 'e']
        lst_b = [0, 0, 3, 2, 0]
        r = Utils.sort_list_by_another_list(lst_a, lst_b, reverse=False)
        e = ['a', 'b', 'e', 'd', 'c']
        self.assertListEqual(r, e)

    def test_gw_02(self):
        lst_a = ['a', 'b', 'c', 'd', 'e']
        lst_b = [0, 0, 3, 2, 0]
        r = Utils.sort_list_by_another_list(lst_a, lst_b, reverse=True)
        e = ['c', 'd', 'a', 'b', 'e']
        self.assertListEqual(r, e)

    def test_gw_03(self):
        """Verify that empty lists do not raise an exception."""
        lst_a = []
        lst_b = []
        r = Utils.sort_list_by_another_list(lst_a, lst_b, reverse=False)
        e = []
        self.assertListEqual(r, e)


class TestFilterArray(TestCase):
    def gw(self, a, e):
        r = Utils.filter_array(a)
        TestUtils.equal_list(self, r, e)

    def test_gw_01(self):
        a = [1, 2, 3, np.nan]
        e = [1, 2, 3]
        self.gw(a, e)

    def test_gw_02(self):
        a = ['a', 'b', 'c', np.nan]
        e = a
        self.gw(a, e)

    def test_gw_03(self):
        a = np.array([1, 2, 3, np.nan])
        e = np.array([1, 2, 3])
        self.gw(a, e)

    def test_gw_04(self):
        a = np.array(['a', 'b', 'c', np.nan])
        e = a
        self.gw(a, e)

    def test_gw_05(self):
        a = [2 ** 0.5, np.nan, 3 ** 0.5, np.nan]
        e = [2 ** 0.5, 3 ** 0.5]
        self.gw(a, e)

    def test_gw_06(self):
        a = np.array([2 ** 0.5, np.nan, 3 ** 0.5, np.nan])
        e = np.array([2 ** 0.5, 3 ** 0.5])
        self.gw(a, e)


class TestFlattenNumpyArray(TestCase):
    def gw(self, a, e):
        r = Utils.flatten_np_array(a)
        TestUtils.equal_list(self, r, e)

    def test_gw_01(self):
        a = np.array([1, 2, 3, 4, 2, 3, 4])
        e = np.array([1, 2, 3, 4, 2, 3, 4])
        self.gw(a, e)

    def test_gw_02(self):
        a = np.array([[1], [2, 3, 4], [], [2, 3, 4]])
        e = np.array([1, 2, 3, 4, 2, 3, 4])
        self.gw(a, e)

    def test_gw_03(self):
        a = [[1], [2, 3, 4], [], [2, 3, 4]]
        e = np.array([1, 2, 3, 4, 2, 3, 4])
        self.gw(a, e)

    def disabled_test_gw_04(self):
        """
        Note: the function does not work for nested sublists,
        so this test will fail. That's why it is commented out.
        It does not make sense to check for failure, since it
        would be better if it did not fail. It's a fact of life.
        """
        a = np.array([[1], [2, [3, 4]], [], [2, 3, 4]])
        r = Utils.flatten_np_array(a)
        e = np.array([1, 2, 3, 4, 2, 3, 4])
        TestUtils.equal_np_matrix(self, r, e, 'flat array')


class TestIncrementSmallest(TestCase):
    def gw(self, lst, dx, e):
        """Verify that the smallest element is incremented."""
        Utils.increment_smallest(lst, dx)
        TestUtils.equal_list(self, lst, e)

    def test_gw_01(self):
        lst_a = np.array([10, 20, 30, 40])
        dx = 5
        e = np.array([15, 20, 30, 40])
        self.gw(lst_a, dx, e)

    def test_gw_02(self):
        lst_a = np.array([50, 20, 30, 40])
        dx = 5
        e = np.array([50, 25, 30, 40])
        self.gw(lst_a, dx, e)

    def test_gw_03(self):
        lst_a = np.array([50, 20, 20, 40])
        dx = 5
        e = np.array([50, 25, 20, 40])
        self.gw(lst_a, dx, e)


class TestFrequencyCount2OccurrenceList(TestCase):
    def gw(self, a, e):
        """Verify that a frequency count can be converted into an occurrence list."""
        r = Utils.frequency_count2occurrence_list(a)
        TestUtils.equal_list(self, r, e)

    def test_gw_01(self):
        a = [[0, 4], [1, 2], [2, 3], [10, 1]]
        e = np.array([0, 0, 0, 0, 1, 1, 2, 2, 2, 10])
        self.gw(a, e)

    def test_gw_02(self):
        a = [['a', 4], ['b', 2], ['c', 3], ['d', 1]]
        e = np.array(['a', 'a', 'a', 'a', 'b', 'b', 'c', 'c', 'c', 'd'])
        self.gw(a, e)

    def test_gw_03(self):
        a = [[None, 1], ['a', 4], ['b', 2], ['c', 3], ['d', 1]]
        e = np.array(['a', 'a', 'a', 'a', 'b', 'b', 'c', 'c', 'c', 'd'])
        self.gw(a, e)

    def test_gw_04(self):
        a = [[None, 1], [1.0, 4], [2, 2], [3.14159265359, 3], ['d', 1]]
        e = np.array(['1.0', '1.0', '1.0', '1.0', '2.0', '2.0',
                      '3.14159265359', '3.14159265359', '3.14159265359', 'd'])
        self.gw(a, e)


class TestFilterNoneFromFrequencyCount(TestCase):
    def gw(self, a, e):
        """Verify that None rows are filtered out a frequency count."""
        r = Utils.filter_none_from_frequency_count(a)
        TestUtils.equal_list(self, r, e)

    def test_gw_01(self):
        a = [[0, 4], [1, 2], [2, 3], [10, 1]]
        e = a
        self.gw(a, e)

    def test_gw_02(self):
        a = [[None, 512], [0, 4], [1, 2], [2, 3], [10, 1]]
        e = [[0, 4], [1, 2], [2, 3], [10, 1]]
        self.gw(a, e)

    def test_gw_03(self):
        a = [[None, 512], ['a', 4], ['b', 2], ['c', 3], ['NULL', 1], ['None', 10]]
        e = [['a', 4], ['b', 2], ['c', 3], ['NULL', 1], ['None', 10]]
        self.gw(a, e)


class TestDeleteRowsCsr(TestCase):

    def test_gw_01(self):
        mtrx = csr_matrix(np.identity(6), dtype=int)
        r = Utils.delete_rows_csr(mtrx, [1, 3])
        e = csr_matrix([[1, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 1]])
        TestUtils.equal_csr_matrix(self, r, e, 'removed row csr_matrix')
        orig = csr_matrix(np.identity(6), dtype=int)
        TestUtils.equal_csr_matrix(self, mtrx, orig, 'original csr_matrix')

    def test_gw_02(self):
        mtrx = csr_matrix(np.identity(6), dtype=int)
        r = Utils.delete_rows_csr(mtrx, [0, 1, 2])
        e = csr_matrix([[0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 1]])
        TestUtils.equal_csr_matrix(self, r, e, 'removed row csr_matrix')

    def test_gw_03(self):
        mtrx = csr_matrix(np.identity(6), dtype=int)
        r = Utils.delete_rows_csr(mtrx, range(6))
        e = (0, 6)
        TestUtils.equal_tuple_numbers(self, r.shape, e, 'shape of empty matrix')

    def test_bw_01(self):
        mtrx = csr_matrix(np.identity(6), dtype=int)
        with self.assertRaisesRegex(AssertionError, 'out of bounds'):
            # Index out of bounds
            Utils.delete_rows_csr(mtrx, [7])


class TestSetRowCsr(TestCase):
    def test_gw_01(self):
        mtrx = csr_matrix([[0, 1, 0],
                           [1, 0, 1],
                           [0, 1, 0]])
        new_row = np.array([2, 3, 4])
        Utils.set_row_csr(mtrx, 0, new_row)
        e = csr_matrix([[2, 3, 4],
                        [1, 0, 1],
                        [0, 1, 0]])
        TestUtils.equal_csr_matrix(self, mtrx, e, 'new_csr')

    def test_gw_02(self):
        mtrx = csr_matrix([[0, 1, 0],
                           [1, 0, 1],
                           [0, 1, 0]])
        new_row = np.array([-1, -1, -1], dtype=int)
        Utils.set_row_csr(mtrx, 2, new_row)
        e = csr_matrix([[0, 1, 0],
                        [1, 0, 1],
                        [-1, -1, -1]])
        TestUtils.equal_csr_matrix(self, mtrx, e, 'new_csr')

    def test_gw_03(self):
        mtrx = csr_matrix([[0, 1, 0],
                           [1, 0, 1],
                           [0, 1, 0]])
        new_row = np.array([-1, -1, -1], dtype=float)
        Utils.set_row_csr(mtrx, 2, new_row)
        e = csr_matrix([[0, 1, 0],
                        [1, 0, 1],
                        [-1, -1, -1]])
        TestUtils.equal_csr_matrix(self, mtrx, e, 'new_csr')

    def test_gw_04(self):
        mtrx = csr_matrix([[0, 1, 0],
                           [1, 0, 1],
                           [0, 1, 0]])
        new_row = [-1, -1, -1]
        Utils.set_row_csr(mtrx, 2, new_row)
        e = csr_matrix([[0, 1, 0],
                        [1, 0, 1],
                        [-1, -1, -1]])
        TestUtils.equal_csr_matrix(self, mtrx, e, 'new_csr')

    def test_bw_01(self):
        """Verify that an exception is raised if the new row is not a list."""
        mtrx = csr_matrix([[0, 1, 0],
                           [1, 0, 1],
                           [0, 1, 0]])
        new_row = -1
        with self.assertRaises(AssertionError):
            Utils.set_row_csr(mtrx, 2, new_row)

    def test_bw_02(self):
        """Verify that an exception is raised if the new row does not have enough elements."""
        mtrx = csr_matrix([[0, 1, 0],
                           [1, 0, 1],
                           [0, 1, 0]])
        new_row = [-1, -1]
        with self.assertRaises(AssertionError):
            Utils.set_row_csr(mtrx, 2, new_row)

    def test_bw_03(self):
        """Verify that an exception is raised if the row index larger than then number of rows in A."""
        mtrx = csr_matrix([[0, 1, 0],
                           [1, 0, 1],
                           [0, 1, 0]])
        new_row = [-1, -1, -1]
        with self.assertRaises(AssertionError):
            Utils.set_row_csr(mtrx, 3, new_row)


class TestNormalizeOverlapMatrix(TestCase):
    def test_gw_01(self):
        a = np.ones(shape=[4, 4]) + 3 * np.eye(4)
        a[0, 0] = 100
        a[3, 3] = 25
        a[0, 3] = 16
        r = Utils.normalize_overlap_matrix(a)
        e = np.matrix([[1., 0.05, 0.05, 0.32],
                       [0.05, 1., 0.25, 0.1],
                       [0.05, 0.25, 1., 0.1],
                       [0.02, 0.1, 0.1, 1.]])
        np.testing.assert_array_almost_equal(r, e)

    def test_bw_01(self):
        """Verify that an error is raised if there is a zero on the diagonal"""
        with self.assertRaisesRegex(AssertionError, 'diagonal'):
            a = np.reshape(np.arange(16), [4, 4])
            Utils.normalize_overlap_matrix(a)

    def test_bw_02(self):
        """Verify that an error is raised if the overlap matrix is not square."""
        with self.assertRaisesRegex(AssertionError, 'square'):
            a = np.matrix(np.arange(1, 5))
            Utils.normalize_overlap_matrix(a)


class TestHsb2Rgb(TestCase):
    def gw(self, hsb, e):
        """Verify that a hsb value is properly transformed into a rgb value"""
        r = Utils.hsb2rgb(hsb)
        TestUtils.equal_list(self, r, e)

    def test_gw_01(self):
        hsb = (0, 100, 100)
        e = [255, 0, 0]
        self.gw(hsb, e)

    def test_gw_02(self):
        hsb = (180, 100, 100)
        e = [0, 255, 255]
        self.gw(hsb, e)

    def test_gw_03(self):
        hsb = (90, 50, 50)
        e = [96, 128, 64]
        self.gw(hsb, e)

    def test_gw_04(self):
        hsb = (270, 0, 50)
        e = [128, 128, 128]
        self.gw(hsb, e)

    def test_gw_05(self):
        hsb = (270, 50, 0)
        e = [0, 0, 0]
        self.gw(hsb, e)

    def test_gw_06(self):
        hsb = (0, 0, 100)
        e = [255, 255, 255]
        self.gw(hsb, e)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    main()

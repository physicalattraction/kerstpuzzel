from unittest import TestCase

from prime import is_prime, nth_prime, prime_factorize


class PrimeTestCase(TestCase):
    def test_is_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(269))

        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(6))
        self.assertFalse(is_prime(9))
        self.assertFalse(is_prime(1000))

    def test_nth_prime(self):
        self.assertEqual(2, nth_prime(1))
        self.assertEqual(3, nth_prime(2))
        self.assertEqual(5, nth_prime(3))
        self.assertEqual(13, nth_prime(6))
        self.assertEqual(1223, nth_prime(200))
        self.assertEqual(224737, nth_prime(20000))

    def test_prime_factorize(self):
        self.assertEqual([2], prime_factorize(2))
        self.assertEqual([3], prime_factorize(3))
        self.assertEqual([2, 2], prime_factorize(4))
        self.assertEqual([2, 2, 3, 3, 5, 5, 224737], prime_factorize(2 * 2 * 3 * 3 * 5 * 5 * 224737))

import re
from unittest import TestCase

from regexer import DictionaryRegexer


class DictionaryRegexerTestCase(TestCase):
    def setUp(self):
        self.regexer = DictionaryRegexer()

    def test_pattern_to_regex(self):
        self.assertEqual('abc...ghi', self.regexer.pattern_to_regexp('abc...ghi'))
        self.assertEqual('abc...ghi', self.regexer.pattern_to_regexp('abc*ghi'))

    def test_regex(self):
        self.assertEqual(['ABC', 'abc'], re.findall('abc', 'ABC\nabc', re.IGNORECASE))
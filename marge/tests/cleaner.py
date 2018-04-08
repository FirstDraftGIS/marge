import json
import unittest

from marge.cleaner import *

class TestCleaner(unittest.TestCase):

    def test_has(self):
        data = { }
        actual = has(data, "enwiki_tile")
        expected = 0
        self.assertEqual(actual, expected)

        data = { "enwiki_tile": "" }
        actual = has(data, "enwiki_tile")
        expected = 0
        self.assertEqual(actual, expected)

        data = { "enwiki_tile": "Spain" }
        actual = has(data, "enwiki_tile")
        expected = 1
        self.assertEqual(actual, expected)

    def test_has_over(self):
        data = { "population": '147629' }
        actual = has_over(data, "population", 1e2)
        expected = 1
        self.assertEqual(actual, expected)

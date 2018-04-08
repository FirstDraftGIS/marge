import json
import unittest

from marge.enricher import enrich

class TestEnricher(unittest.TestCase):

    def test_in_memory(self):
        data = [
            {
                "population": 12345678
            },
            {

            }
        ]

        expected = [{"population": 12345678, "has_enwiki_title": 0, "has_population_over_1_hundred": 1, "has_population_over_1_thousand": 1, "has_population_over_1_million": 1}, {"has_population_over_1_thousand": 0, "has_enwiki_title": 0, "has_population_over_1_hundred": 0, "has_population_over_1_million": 0}]
        actual = enrich(data, in_memory=True, debug=True)
        print("actual:", actual)
        #self.assertEqual(json.dumps(actual), json.dumps(expected))
        for index, obj in enumerate(expected):
            for key, value in obj.items():
                self.assertEqual(value, actual[index][key])

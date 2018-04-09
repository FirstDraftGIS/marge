from csv import DictReader
import json
from itertools import groupby
from numpy import mean
from pandas import DataFrame
import pprint
import unittest

from marge.config import config
from marge.resolver import *
from marge.models import Model
from marge.utils import to_dicts

pp = pprint.PrettyPrinter(indent=4)

class BaseModelTestCase(unittest.TestCase):

    def setUp(self):
        print("setting up TestFirstPass")
        self.m1 = Model("first_pass")
        self.m2 = Model("second_pass")
        self.test_set = to_dicts(config["files"]["dirty_testing_file"], nrows=config["testing"]["nrows"])

    def score(self, test_set, model):
        scores = []
        try:
            grouped = groupby(test_set, key=lambda x: x["order_id"])
        except Exception as e:
            print(e)
            raise(e)
        for order_id, order in grouped:
            num_incorrect = 0
            num_correct = 0
            for feature_id, features in groupby(order, key=lambda x: x["feature_id"]):
                #print("\n\n\nfeature_id:", feature_id)
                #pp.pprint(list(features))
                results = model.predict(list(features))
                if results is not None:
                    rows = [row for row_index, row in results.iterrows()]
                    if rows:
                        max_probability = max([row["probability"] for row in rows])
                        correct_rows = [row for row in rows if row["correct"]]
                        if correct_rows:
                            correct = correct_rows[0]
                            # do I have to worry about floating point arithmetic??
                            if correct["probability"] == max_probability:
                                num_correct += 1
                            else:
                                num_incorrect += 1
                        else:
                            num_incorrect += 1

            total = num_correct + num_incorrect
            if total:
                score = float(num_correct) / total
                scores.append(score)
        mean_score = mean(scores)
        print("len(score:", scores)
        self.assertTrue(len(scores) > 10)
        return mean_score


class TestFirstPass(BaseModelTestCase):
    def test_first_pass(self):
        print("\n\n\nstarting test_first_pass")
        mean_score = self.score(self.test_set, self.m1)
        print("m1 mean_score:", round(mean_score,2))
        self.assertTrue(mean_score > 0.9)

class TestSecondPass(BaseModelTestCase):
    def test_second_pass(self):
        print("\n\n\nstarting test_second_pass")
        first_results = to_dicts(self.m1.predict(self.test_set))
        mean_score = self.score(first_results, self.m2)
        print("m2 mean_score:", round(mean_score,2))
        self.assertTrue(mean_score > 0.95)

from csv import DictReader
import json
from itertools import groupby
from numpy import mean
from pandas import DataFrame
import pprint
import unittest

from marge.config import config
from marge.enricher import *
from marge.resolver import *
from marge.models import Model
from marge.tester import score
from marge.utils import *


pp = pprint.PrettyPrinter(indent=4)

# https://en.wikipedia.org/wiki/Precision_and_recall#Introduction
class BaseModelTestCase(unittest.TestCase):

    def setUp(self):
        print("setting up TestFirstPass")
        self.m1 = Model("first_pass")
        self.m2 = Model("second_pass")
        self.m3 = Model("third_pass")
        self.test_set = to_dicts(config["files"]["dirty_testing_file"], nrows=config["testing"]["nrows"])

    def run_pipeline(self, places, num_steps=0):
        if num_steps >= 1:
            places = combine_fields(places, ["order_id", "feature_id"])
        if num_steps >= 2:
            places = to_dicts(self.m1.predict(places))
            places = add_or_update_most_likely_correct(places)
            places = add_median_cooccurrence(places)
        if num_steps >= 3:
            places = to_dicts(self.m2.predict(places))
            places = add_or_update_most_likely_correct(places)
            places = add_is_a_place_frequency(places)

        return places

class TestFirstPass(BaseModelTestCase):
    def test_first_pass(self):
        print("\n\n\nstarting test_first_pass")
        places = self.run_pipeline(self.test_set, num_steps=1)

        f1s = []
        for places_by_order in group_by(places, "order_id"):
            counter = Counter()
            for options in group_by(places_by_order, "feature_id"):
                results = self.m1.predict(list(options))
                if results is not None:
                    rows = [row for row_index, row in results.iterrows()]
                    if rows:
                        max_score = max([row["score_1"] for row in rows])
                        selection = next(row for row in rows if row["score_1"] == max_score)
                        counter["positives"] += 1
                        if selection["correct"] == 1:
                            counter["true positives"] += 1
                        elif selection["correct"] == 0:
                            counter["false positives"] += 1
            precision = counter["true positives"] / counter["positives"]
            recall = counter["true positives"] / (counter["true positives"] + counter["false negatives"])
            f1 = 2 * ((precision * recall) / (precision + recall))
            f1s.append(f1)
        mean_f1_score = mean(f1s)
        print("mean_f1_score after first run", mean_f1_score)
        self.assertTrue(mean_f1_score > 0.5)

class TestSecondPass(BaseModelTestCase):
    def test_second_pass(self):
        print("\n\n\nstarting test_first_pass")
        places = self.run_pipeline(self.test_set, num_steps=2)

        f1s = []
        for places_by_order in group_by(places, "order_id"):
            counter = Counter()
            for options in group_by(places_by_order, "feature_id"):
                results = self.m2.predict(list(options))
                if results is not None:
                    rows = [row for row_index, row in results.iterrows()]
                    if rows:
                        max_score = max([row["score_2"] for row in rows])
                        selection = next(row for row in rows if row["score_2"] == max_score)
                        counter["positives"] += 1
                        if selection["correct"] == 1:
                            counter["true positives"] += 1
                        elif selection["correct"] == 0:
                            counter["false positives"] += 1
            precision = counter["true positives"] / counter["positives"]
            recall = counter["true positives"] / (counter["true positives"] + counter["false negatives"])
            f1 = 2 * ((precision * recall) / (precision + recall))
            f1s.append(f1)
        mean_f1_score = mean(f1s)
        print("mean_f1_score after second run", mean_f1_score)
        self.assertTrue(mean_f1_score > 0.5)

class TestThirdPass(BaseModelTestCase):
    def test_third_pass(self):
        print("\n\n\nstarting test_third_pass")
        places = self.run_pipeline(self.test_set, num_steps=3)

        f1s = []
        for places_by_order in group_by(places, "order_id"):
            counter = Counter()
            for options in group_by(places_by_order, "feature_id"):
                results = self.m3.predict(list(options))
                if results is not None:
                    rows = [row for row_index, row in results.iterrows()]
                    if rows:
                        max_score = max([row["score_2"] for row in rows])
                        selection = next(row for row in rows if row["score_2"] == max_score)
                        placehood = selection["score_3"] > 0.5
                        if placehood:
                            counter["positives"] += 1
                            if selection["correct"] == 1:
                                counter["true positives"] += 1
                            else:
                                counter["false positives"] += 1
                        else:
                            if selection["correct"]:
                                counter["false negatives"] += 1
                            else:
                                counter["true negatives"] += 1
                            counter["false positives"] += 1
            precision = counter["true positives"] / counter["positives"]
            recall = counter["true positives"] / (counter["true positives"] + counter["false negatives"])
            f1 = 2 * ((precision * recall) / (precision + recall))
            f1s.append(f1)
        mean_f1_score = mean(f1s)
        print("mean_f1_score after second run", mean_f1_score)
        self.assertTrue(mean_f1_score > 0.5)
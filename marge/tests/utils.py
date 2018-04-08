import json
import unittest

from marge.utils import *

class TestUtils(unittest.TestCase):

    def test_has_enwiki_title(self):
        train_set = to_dicts(config["files"]["dirty_training_file"], nrows=2000)
        count = 0
        for d in train_set:
            if "enwiki_title" in d:
                count += 1
            else:
                print("enwiki_title not in ", d)
        self.assertTrue(count > 100)

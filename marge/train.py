import pprint

from enricher import add_or_update_most_likely_correct, add_median_cooccurrence, combine_fields
from enricher import add_is_a_place_frequency

from marge.config import config
from marge.utils import to_dicts
from marge.models import Model

pp = pprint.PrettyPrinter(indent=4)

m1 = Model("first_pass")
m1.train()
train_set = to_dicts(config["files"]["dirty_training_file"], nrows=config["training"]["rowcount"])
places = combine_fields(train_set, ["order_id", "feature_id"])
places = m1.predict(train_set)
print('done with first pass')

places = add_or_update_most_likely_correct(places)
places = add_median_cooccurrence(places)

m2 = Model("second_pass")
print("m2:", m2)
m2.train(train_set=places)
places = m2.predict(places)
print("done with second pass")

places = add_or_update_most_likely_correct(places)
places = add_is_a_place_frequency(places)

from collections import Counter
counts = Counter([p["is_a_place_frequency"] for p in places])

pp.pprint(counts)

m3 = Model("third_pass")
print("m3:", m3)

"""
    We only need those most likely to be correct by name
    because we're not deciding which option to pick here,
    but whether the option is a place or not
"""
places = [place for place in places if place["most_likely_correct"] == 1]

places = m3.train(train_set=places)


print("FINISHED TRAINING\n\n\n\n\n")

from enricher import add_likely_correct, add_median_cooccurrence, combine_fields

from marge.config import config
from marge.utils import to_dicts
from marge.models import Model

m1 = Model("first_pass")
m1.train()
train_set = to_dicts(config["files"]["dirty_training_file"], nrows=config["training"]["rowcount"])
places = combine_fields(train_set, ["order_id", "feature_id"])
first_results = m1.predict(train_set)
print('first_results:', first_results)

places = add_likely_correct(first_results)
places = add_median_cooccurrence(places)

m2 = Model("second_pass")
print("m2:", m2)
m2.train(train_set=places)
#second_results = m2.predict(first_results)
print("m2 trained:", m2)

print("FINISHED TRAINING\n\n\n\n\n")

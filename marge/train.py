from marge.config import config
from marge.utils import to_dicts
from marge.models import Model

m1 = Model("first_pass")
m1.train()
train_set = to_dicts(config["files"]["dirty_training_file"], nrows=config["training"]["rowcount"])
first_results = m1.predict(train_set)
#print('first_results:', first_results)

m2 = Model("second_pass")
print("m2:", m2)
m2.train(train_set=first_results)
#second_results = m2.predict(first_results)
print("m2 trained:", m2)

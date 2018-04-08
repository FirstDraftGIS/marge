from marge.config import config
from marge.utils import to_dicts
from marge.models import Model

m1 = Model("first_pass")
m1.train()
"""
train_set = to_dicts(config["files"]["dirty_training_file"], nrows=2000)

# removes excess keys
trimmed = m1.trim_dicts(train_set)

# removes items if have null keys
filtered = m1.filter_dicts(trimmed)

df = m1.predict(filtered)
print('df:', df)

# get_country_code_ranks

m2 = Model("second_pass")
df = m2.
"""
"""
train_set = pd.read_csv(PROCESSED_TRAINING_FILE, sep="\t").dropna()#.fillna(0)

print("train_set:", train_set)

label = "correct"

Y = train_set[label]
print("Y:", Y)

difference = train_set.columns.difference([label])
print("difference:", difference)


X = train_set[difference]

#X = train_set["count_additions"].reshape(-1, 1)
print("X:", X)

model = LinearRegression()
model.fit(X, Y)

print("fitted")

print("model._intercept", dir(model))
print("difference:", difference)
print("model._intercept", model.intercept_)
print("model._intercept", model.coef_)
print("model._intercept", model.get_params())

with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)
"""

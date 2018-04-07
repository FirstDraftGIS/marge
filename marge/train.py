import numpy as np
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle
import math

from config import *

train_set = pd.read_csv(PROCESSED_TRAINING_FILE, sep="\t").dropna()#.fillna(0)

print("train_set:", train_set)

label = "correct"

model = LinearRegression()

Y = train_set[label]
print("Y:", Y)

difference = train_set.columns.difference([label])
print("difference:", difference)


X = train_set[difference]

#X = train_set["count_additions"].reshape(-1, 1)
print("X:", X)

model.fit(X, Y)

print("fitted")

print("model._intercept", dir(model))
print("difference:", difference)
print("model._intercept", model.intercept_)
print("model._intercept", model.coef_)
print("model._intercept", model.get_params())

with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

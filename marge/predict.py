import pickle
from numpy import argmax

from config import MODEL_PATH

def get_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

def predict(X, model=None):

    if model is None:
        model = get_model()

    predictions = model.predict(X)

    return predictions

def select(X, model=None):

    if model is None:
        model = get_model()

    predictions = model.predict(X)
    #print("predictions:", predictions)
    maxindex = argmax(predictions, axis=0)
    return maxindex

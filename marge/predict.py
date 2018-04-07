import pickle
from numpy import argmax

from .config import MODEL_PATH

def get_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

def get_probabilities(X, model=None):

    if model is None:
        model = get_model()

    get_probabilities = model.predict(X)

    return get_probabilities

def select(X, model=None):

    if model is None:
        model = get_model()

    probabilities = model.get_probabilities(X)
    #print("probabilities:", probabilities)
    maxindex = argmax(probabilities, axis=0)
    return maxindex

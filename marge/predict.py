import pickle
from numpy import argmax

from .config import MODEL_PATH


def get_probabilities(X, model=None):

    try:

        print("starting get probabilities with", X)

        if model is None:
            model = get_model()

        num_actual_columns = len(X.columns)
        num_expected_columns = len(model.coef_)
        if num_actual_columns != num_expected_columns:
            raise Exception("[marge] expected " + str(num_expected_columns) + " columns but got " + str(num_actual_columns) + " instead.")


        get_probabilities = model.predict(X)

        return get_probabilities

    except Exception as e:
        print("[marge] get_probabilities hit an error:", e)

def select(X, model=None):

    if model is None:
        model = get_model()

    probabilities = model.get_probabilities(X)
    #print("probabilities:", probabilities)
    maxindex = argmax(probabilities, axis=0)
    return maxindex

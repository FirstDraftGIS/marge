from pandas import DataFrame, read_csv
import pickle
from sklearn.linear_model import LinearRegression

from config import config
from marge.enricher import enrich
from marge.utils import to_dicts

class Model:

    def __init__(self, name):
        self.config = config["models"][name]

    def convert(self, i):
        return i if isinstance(i, DataFrame) else DataFrame(i)

    # filter out dicts who have None in one of the relevant columns
    def filter_dicts(self, dicts):
        #return [d for d in dicts if all(v not in [None, ""] for v in d.values())]
        results = []
        for d in dicts:
            keep = True
            for key, value in d.items():
                if key in self.config["columns"] and value in [None, ""]:
                    keep = False
            if keep:
                results.append(d)
        return results

    def load(self):
        with open(self.config["path"], "rb") as f:
            return pickle.load(f)

    def predict(self, i):
        dicts = enrich(i, in_memory=True)
        df = self.convert(dicts)
        df = self.trim(df)
        df["prediction"] = self.load().predict(df)
        return df

    def train(self, train_set=None):
        if train_set is None:
            train_set = to_dicts(config["files"]["dirty_training_file"], nrows=2000)
        dicts = enrich(train_set, in_memory=True)
        filtered = self.filter_dicts(dicts)
        df = self.convert(filtered)
        model = LinearRegression()
        X = self.trim(df)
        Y = df["correct"]
        model.fit(X, Y)
        print("weights", dict(zip(self.config["columns"], model.coef_)))
        with open(self.config["path"], "wb") as f:
            pickle.dump(model, f)

    def trim(self, df):
        return df[self.config["columns"]]

    def trim_dicts(self, dicts, columns=None):
        columns = self.config["columns"] + ["correct"]
        return [
            dict([(k, v) for k, v in d.items() if k in columns ])
            for d in dicts
        ]

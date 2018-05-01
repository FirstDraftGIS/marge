from georich import enrich
from numpy import where
from pandas import DataFrame, read_csv
import pprint
import pickle
from sklearn.linear_model import LinearRegression, LogisticRegression, SGDRegressor
from sklearn.tree import DecisionTreeRegressor

from marge.config import config
from marge.utils import get_absolute_path, to_dicts

pp = pprint.PrettyPrinter(indent=4)

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
                    #print("not keeping kv", [key], [value])
                    keep = False
            if keep:
                results.append(d)
        return results

    def load(self):
        with open(get_absolute_path(self.config["path"]), "rb") as f:
            return pickle.load(f)

    def predict(self, inpt):
        dicts = enrich(inpt, new_fields=self.config["columns"], in_memory=True)
        filtered = self.filter_dicts(dicts)
        if filtered:
            df = self.convert(filtered)
            trimmed = self.trim(df)
            df["score"] = self.load().predict(trimmed)
            return df

    def train(self, train_set=None):
        if train_set is None:
            train_set = to_dicts(config["files"]["dirty_training_file"], nrows=2000)
        dicts = enrich(train_set, new_fields=self.config["columns"], in_memory=True)
        filtered = self.filter_dicts(dicts)
        print("filtered")
        #pp.pprint(filtered)
        df = self.convert(filtered)
        model = LinearRegression()
        #model = SGDRegressor()
        #model = LogisticRegression()
        #model = DecisionTreeRegressor()
        X = self.trim(df)
        self.validate_df(X)
        Y = df["correct"]
        print("Y:", Y.dtypes)
        print("Y:", set(Y))
        model.fit(X, Y)
        #pp.pprint(model.coef_)
        pp.pprint(dict(zip(self.config["columns"], [round(n, 2) for n in model.coef_])))
        with open(get_absolute_path(self.config["path"]), "wb") as f:
            pickle.dump(model, f)

    def trim(self, df):
        return df[self.config["columns"]]

    def trim_dicts(self, dicts, columns=None):
        columns = self.config["columns"] + ["correct"]
        return [
            dict([(k, v) for k, v in d.items() if k in columns ])
            for d in dicts
        ]

    def validate_df(self, df):
        print("validating df")
        for name in self.config["columns"]:
            if len(set(df[name])) == 1:
                raise Exception("UH OH: there's only one in the set for " + name)

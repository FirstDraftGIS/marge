from config import config

class Model:
    def __init__(self, name):
        self.config = config["models"][name]
        print("self.config:", self.config)
    def convert(self, i):
        return i if isinstance(i, DataFrame) else DataFrame(i)
    def trim(self, df):
        return df[config["models"][self.config["model_name"]]["columns"]]
    def load(self):
        with open(self.config["path"], "rb") as f:
            return pickle.load(f)
    def predict(self, i):
        df = self.convert(i)
        df = self.trim(df)
        df["prediction"] = self.load().predict()
        return df

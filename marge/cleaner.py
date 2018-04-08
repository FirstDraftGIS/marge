from datetime import datetime
from pandas import read_csv
from .utils import *

from marge.config import config
from .enumerations import *

# cleans data frame for first pass
# basically, removes any unnecessary columns
def trim(df, model_name):
    keeping_these_columns = config["models"][model_name]["columns"]
    return df[keeping_these_columns]

# gets value for a given key
def get_value(i, key):
    if isinstance(i, dict):
        return i.get(key, None)
    elif hasattr(i, key):
        return i.key

def simple_has(obj, key):
    return 1 if get_value(obj, key) not in nulls else 0

def has(obj, key):
    return simple_has(obj, "has_" + key) or simple_has(obj, key)

def has_over(obj, key, threshold):
    value = get_value(obj, key)
    if value in nulls:
        return 0
    elif isinstance(value, int) or isinstance(value, float):
        return 1 if value > threshold else 0
    elif isinstance(value, str) and value.isdigit():
        return 1 if int(value) > threshold else 0
    else:
        return 0

def tofloat(i):
    if isinstance(i, float):
        return i
    elif isinstance(i, int):
        return float(int)
    elif isinstance(i, str):
        return float(i.replace(",", ""))

def is_truthy(i):
    return 1 if i in truthies else 0

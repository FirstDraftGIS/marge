from collections import Counter
from csv import DictReader
from os.path import expanduser
from pandas import DataFrame
import json

from marge.config import config
from marge.enumerations import *
from marge.enumerations import incompletes

def get_absolute_path(path):
    if path.startswith("~"):
        return expanduser(path)
    else:
        return path

def clone(obj):
    return json.loads(json.dumps(obj))


def truthify(x):
    return 0 if x in [None, "", False, "false"] else 1

def is_admin(row):

    try:
        if "geonames_feature_class" in row and row["geonames_feature_class"] == "A":
            return 1

        for key in ["admin_level"]:
            if key in row and row[key]:
                return 1
            try:
                if int(row[key]) > 0:
                    return 1
            except:
                return 0

        return 0
    except Exception as e:
        print(row)
        print(e)
        raise(e)

def is_country(row):
    try:
        if int(row['admin_level']) <= 2:
            return 1
        else:
            return 0
    except:
        return 0

def has_pop_over(entity, threshold):
    try:
        if hasattr(entity, "population"):
            if int(entity.population) > threshold:
                return 1
            else:
                return 0
        elif int(entity["population"]) > threshold:
            return 1
        else:
            return 0
    except:
        return 0

def numerify(obj):
    for key, value in obj.items():
        if isinstance(value, str):
            if value == "":
                obj[key] = 0
            else:
                try:
                    obj[key] = float(value)
                except:
                    pass
    return obj


def get_model(model_name):
    with open(get_absolute_path(MODEL_PATH), "rb") as f:
        return pickle.load(fail)

def to_dicts(inpt, nrows=None):
    dicts = []
    if isinstance(inpt, str):
        print("to_dicts filepath:", inpt)
        with open(get_absolute_path(inpt)) as f:
            reader = DictReader(f, delimiter="\t")
            count = 0
            for row in reader:
                count += 1
                if nrows and count > nrows:
                    break
                dicts.append(row)
    elif isinstance(inpt, DataFrame):
        count = 0
        for index, series in inpt.iterrows():
            count += 1
            if nrows and count > nrows:
                break
            dicts.append(series.to_dict())
    return dicts


def max_by_group(iterator, column_name, group_name):
    try:
        maxes = {}
        for item in iterator:
            gid = item[group_name]
            value = item[column_name]
            if gid not in maxes or value > maxes[gid]:
                maxes[gid] = value
        return maxes
    except Exception as e:
        print("max_by_group failed with", e)

def is_complete(item):
    if isinstance(item, str):
        return item not in ["", "blank", "null", "Null", "NULL", "NONE", "none", "None"]
    elif isinstance(item, float) or isinstance(item, int):
        return True
    elif item != None:
        return True
    else:
        return False

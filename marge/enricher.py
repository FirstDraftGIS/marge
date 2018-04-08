from collections import Counter
from freq import Freq
from itertools import _grouper
from os.path import isfile
from pandas import DataFrame
import csv

from .cleaner import has, has_over, is_truthy, simple_has
from .utils import max_by_group

"""
    This method enriches the file by:
        - converting fields to 1 and 0
        - adding additional fields

    This is basically prepping a file so it can be put into a dataframe
"""
def enrich(i, save_path=None, in_memory=False, debug=False):

    if debug:
        print("starting enricher")
        print("\ti:", i)
        print("\tsave_path:", save_path)
        print("\tin_memory:", in_memory)
        print("\tdebug:", debug)

    # convert input to list of dicts
    if isinstance(i, list) and isinstance(i[0], dict):
        iterator = i
        keys = list(i[0].keys())
    elif isinstance(i, DataFrame):
        iterator = list([series.to_dict() for index, series in i.iterrows()])
        keys = list(iterator[0].keys())
    elif isinstance(i, str) and isfile(i):
        sep = "\t" if i.endswith("\t") else ","
        f = open(i)
        iterator = csv.DictReader(f, delimiter=sep)
        keys = list(iterator.fieldnames)
    elif isinstance(i, _grouper):
        for thing in _grouper:
            print("thing:", thing)
        iterator = list(_grouper)
        keys = list(iterator[0].keys())

    if debug: print("\titerator:", iterator)

    calc_country_code_frequency = "probability" in keys

    new_keys = [
        "has_enwiki_title",
        "has_population_over_1_million",
        "has_population_over_1_thousand",
        "has_population_over_1_hundred"
    ]

    if calc_country_code_frequency:
        new_keys.append("country_code_frequency")

    fieldnames = list(set(keys + new_keys))

    if debug: print("\tfieldnames:", fieldnames)

    if save_path:
        with open(save_path, "w") as f:
            writer = csv.DictWriter(f, delimiter="\t", fieldnames=fieldnames)
            writer.writerow()

    if in_memory:
        items = []

    if "probability" in keys and "feature_id" in keys:
        maxes = max_by_group(iterator, "probability", "feature_id")
        for item in iterator:
            fid = item["feature_id"]
            prob = item["probability"]
            item["likely_correct"] = 1 if prob == maxes[fid] else 0

    if calc_country_code_frequency:
        all_country_codes = [ i["country_code"].lower() for i in iterator if i["likely_correct"] ]
        freqs = Freq(all_country_codes)
        for item in iterator:
            cc = item["country_code"].lower()
            item["country_code_frequency"] = freqs[cc]

    #print("items:", iterator[:2])


    s = set()
    #tracker = "has_enwiki_title"
    tracker = None
    for item in iterator:
        item["has_enwiki_title"] = simple_has(item, 'enwiki_title')
        if tracker: s.add(item[tracker])
        item["has_population_over_1_million"] = has_over(item, "population", 1e6)
        item["has_population_over_1_thousand"] = has_over(item, "population", 1e3)
        item["has_population_over_1_hundred"] = has_over(item, "population", 1e2)

        """
            Set importance is 0.25 if no importance is set.
            We're doing this because we have to to assign some value.
        """
        if "importance" in item:
            value = item["importance"]
            if value in ["", None]: item["importance"] = 0.25
            else: item["importance"] = float(item["importance"])


        # booleanify
        for key in ["correct","likely_correct"]:
            if key in item:
                item[key] = is_truthy(item[key])

        if save_path:
            writer.writerow(item)

        if in_memory:
            if debug: print("appended:", item)
            items.append(item)

    if in_memory:
        return items

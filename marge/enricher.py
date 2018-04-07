from os.path import isfile
import csv

from .cleaner import has, has_over

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
    elif isinstance(i, DataFrame):
        iterator = i.to_dict()
    elif isinstance(i, str) and isfile(i):
        sep = "\t" if i.endswith("\t") else ","
        f = open(i)
        iterator = csv.DictReader(f, delimiter=sep)

    if debug: print("\titerator:", iterator)

    fieldnames = list(set(list(i[0].keys()) + [
        "has_enwiki_title",
        "has_population_over_1_million",
        "has_population_over_1_thousand",
        "has_population_over_1_hundred"
    ]))

    if debug: print("\tfieldnames:", fieldnames)

    if save_path:
        with open(save_path, "w") as f:
            writer = csv.DictWriter(f, delimiter="\t", fieldnames=fieldnames)
            writer.writerow()

    if in_memory:
        items = []

    for item in iterator:
        item["has_enwiki_title"] = has(item, 'enwiki_tile')
        item["has_population_over_1_million"] = has_over(item, "population", 1e6)
        item["has_population_over_1_thousand"] = has_over(item, "population", 1e3)
        item["has_population_over_1_hundred"] = has_over(item, "population", 1e2)

        if save_path:
            writer.writerow(item)

        if in_memory:
            if debug: print("appended:", item)
            items.append(item)

    if in_memory:
        return items

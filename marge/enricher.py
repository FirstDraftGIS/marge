"""
marge specific geoenrichment
i.e. stuff that wouldn't make sense in georich
"""
import pickle

from collections import defaultdict, Counter
from config import config
from converter import to_list_of_dicts
from numpy import median
from itertools import groupby
from utils import max_by_group

def combine_fields(places, fields):
    places = to_list_of_dicts(places)
    combined_name = "-".join(fields)
    for place in places:
        place[combined_name] = "-".join([place[field] for field in fields])
    return places

def add_likely_correct(places):

    print("starting add_likely_correct with places:", len(places))
    places = to_list_of_dicts(places)
    print("places converted:", len(places))

    old_fields = places[0].keys()

    if "score" in old_fields and "feature_id" in old_fields:
        maxes = max_by_group(places, "score", "order_id-feature_id")
        for place in places:
            gid = place["order_id-feature_id"]
            prob = place["score"]
            place["likely_correct"] = 1 if prob == maxes[gid] else 0

    print("added likely correct to all places")
    return places


def add_median_cooccurrence(places):

    print("starting add_median_cooccurrence")
    places = to_list_of_dicts(places)

    with open(config["files"]["cooccurrences_path"], "rb") as f:
        cooccurrences = pickle.load(f)

    for key, order in groupby(places, lambda place: place["order_id"]):
        places_in_order = list(order)

        #print("len places_in_order:", len(places_in_order))
        #exit()

        enwiki_titles = [p["enwiki_title"] for p in places_in_order if p["enwiki_title"] and p["likely_correct"]]
        totals = defaultdict(Counter)

        for place in places_in_order:
            place_enwiki_title = place["enwiki_title"]
            place["combos"] = []
            for other_enwiki_title in enwiki_titles:
                if place_enwiki_title != other_enwiki_title:
                    key = tuple(sorted([place_enwiki_title, other_enwiki_title]))
                    value = cooccurrences.get(key, 0)
                    place["combos"].append((other_enwiki_title, value))
                    totals[place["feature_id"]][other_enwiki_title] += value

        """
        for each place in the order
        calculate the median percentage of cooccurence with likely places versus alternative features
        """
        for place in places_in_order:
            feature_totals = totals[place["feature_id"]]
            counts = [float(count) / feature_totals[title] for title, count in place["combos"] if feature_totals[title]]

            # defaults to 0.5 if none cooccurred
            place["median_cooccurrence"] = median(counts) if counts else 0.5

            # no need anymore
            del place["combos"]
        #print("places_in_order:", places_in_order)
        #exit()

    print("set cooccurrence scores")

    return places

"""
marge specific geoenrichment
i.e. stuff that wouldn't make sense in georich
"""
from collections import defaultdict, Counter
from itertools import groupby
from numpy import median
import pickle
import pprint


from marge.config import config
from marge.converter import to_list_of_dicts
from marge.utils import get_absolute_path, max_by_group

pp = pprint.PrettyPrinter(indent=4)

def get_latest_score_key(fields):
    score_keys = [field for field in fields if "score_" in field]
    print("score_keys:", score_keys)
    
    if score_keys:
        latest_score_key = sorted(score_keys, key=lambda k: -1 * int(k.split("_")[1]))[0]
        print("latest_score_key:", latest_score_key)
        
        return latest_score_key

def combine_fields(places, fields):
    places = to_list_of_dicts(places)
    combined_name = "-".join(fields)
    for place in places:
        place[combined_name] = "-".join([place[field] for field in fields])
    return places


def add_or_update_most_likely_correct(places):

    print("starting add_or_update_most_likely_correct with places:", len(places))
    places = to_list_of_dicts(places)
    print("places converted:", len(places))

    old_fields = places[0].keys()

    latest_score_key = get_latest_score_key(old_fields)

    if latest_score_key and "feature_id" in old_fields:
        
        if "order_id-feature_id" in old_fields:
            maxes = max_by_group(places, latest_score_key, "order_id-feature_id")
            for place in places:
                gid = place["order_id-feature_id"]
                prob = place[latest_score_key]
                place["most_likely_correct"] = 1 if prob == maxes[gid] else 0
        else: # assume all same order
            max_score = max([place[latest_score_key] for place in places])
            for place in places:
                place["most_likely_correct"] = 1 if place[latest_score_key] == max_score else 0

    print("added likely correct to all places")
    return places


def add_median_cooccurrence(places):

    print("starting add_median_cooccurrence")
    places = to_list_of_dicts(places)

    with open(get_absolute_path(config["files"]["cooccurrences_path"]), "rb") as f:
        cooccurrences = pickle.load(f)

    for key, order in groupby(places, lambda place: place.get("order_id", None)):
        places_in_order = list(order)

        #print("len places_in_order:", len(places_in_order))
        #exit()

        #print("places_in_order:", places_in_order[0:2])
        enwiki_titles = [p["enwiki_title"] for p in places_in_order if p["enwiki_title"] and p["most_likely_correct"]]
        totals = defaultdict(Counter)

        for place in places_in_order:
            place_enwiki_title = place["enwiki_title"]
            place["combos"] = []
            for other_enwiki_title in enwiki_titles:
                if place_enwiki_title != other_enwiki_title:
                    if place_enwiki_title == None or other_enwiki_title == None:
                        value = 0
                    else:
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

# adds frequency that the name of the place is actually meant as a place
def add_is_a_place_frequency(places):
    
    print("starting add_isaplace_frequency")
    places = to_list_of_dicts(places)

    with open(get_absolute_path(config["files"]["is_a_place_frequency_counter"]), "rb") as f:
        freq = pickle.load(f)

    for place in places:
        place["is_a_place_frequency"] = freq.get(place["name"])
        
    return places
    
### add set predicted_correct to 1 if score_2 > 0.5
def add_results(places):
    for place in places:
        place['placehood']
from marge.models import Model
from marge.utils import to_dicts
from marge.enricher import add_likely_correct, add_median_cooccurrence, combine_fields

def resolve(inpt, debug=True):

    print("starting resolve")
    if debug:
        print("\tinpt:", type(inpt))
        print("\tlen(inpt):", len(inpt))
    first_results = Model("first_pass").predict(inpt)
    print("first_results:", first_results)
    places = add_likely_correct(first_results)
    places = add_median_cooccurrence(places)    
    second_results = Model("second_pass").predict(to_dicts(places))
    return second_results
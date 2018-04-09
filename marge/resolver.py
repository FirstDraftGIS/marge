from marge.models import Model
from marge.utils import to_dicts

def resolve(inpt, debug=True):

    print("starting resolve")
    if debug:
        print("\tinpt:", type(inpt))
        print("\tlen(inpt):", len(inpt))
    first_results = Model("first_pass").predict(inpt)
    print("first_results:", first_results)
    second_results = Model("second_pass").predict(to_dicts(first_results))
    return second_results
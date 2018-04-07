from cleaner import trim
from converter import to_data_frame
from models import Model
from pandas import DataFrame

from config import config

"""
    This method takes in input as a DataFrame or list of dictionaries.
    It cleans the columns and runs a first pass assignment of probabilities.
    It then cleans these results and runs a second pass getting probs.
    Finally it returns a dataframe with probabilities assigned to each place
"""
def resolve(i, debug):

    if debug: print('[marge] starting resolver.resolve with', i)

    df = Model("first_pass").predict(i)
    if debug: print("first_pass results:", df)

    ##### add data for second pass

    df = Model("second_pass").predict(df)
    if debug: print("second_pass results:", df)

    return df

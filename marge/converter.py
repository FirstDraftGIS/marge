from pandas import DataFrame

# converts _input to dataframe
def to_data_frame(_input):
    if isinstance(_input, DataFrame):
        return _input
    else:
        try:
            return DataFrame(_input)
        except Exception as e:
            print("failed converting bc:", e)

# converts input into a list of dictionaries
def to_list_of_dicts(i):
    if isinstance(i, list):
        if isinstance(i[0], dict):
            return i
        else:
            print("need to iterator through and convert to dicts")
    elif isinstance(i, DataFrame):
        return i.to_dict('records')
    elif isinstance(i, str):
        if isfile(i):
            sep = "\t" if i.endswith("\t") else ","
            f = open(i)
            iterator = csv.DictReader(f, delimiter=sep)

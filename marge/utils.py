import json

def clone(obj):
    return json.loads(json.dumps(obj))

def truthify(x):
    return 0 if x in [None, "", False, "false"] else 1

def is_admin(row):

    if row["geonames_feature_class"] == "A":
        return 1

    for key in ["admin1_code", "admin2_code", "admin3_code", "admin4_code", "admin5_code", "admin_level"]:
        if key in row and truthify(row[key]):
            return 1

    return 0

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

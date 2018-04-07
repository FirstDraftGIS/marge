"""
KEEPING_FOR_TRAINING = [
#    "country_code",
#    "geonames_feature_class",
#    "geonames_feature_code",
    "importance",
#    "place_type",
#    "population",
    "correct"
]

KEEPING_FOR_TESTING = KEEPING_FOR_TRAINING + ["order_id", "feature_id"]

NEW_FIELDS = [
    "has_enwiki_title",
    #"is_place_type_b",
    "has_population_over_1_million",
    "has_population_over_1_thousand",
    "has_population_over_1_hundred"
    #,
    #"is_admin"
    #"is_country"
]
"""

import yaml
with open("config.yml") as f:
    config = yaml.load(f.read())

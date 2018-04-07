DIRTY_DATA_FILE = "/tmp/firstdraftgis_export.tsv"
DIRTY_TRAINING_FILE = "/tmp/training_dirty.tsv"
DIRTY_TESTING_FILE = "/tmp/testing_dirty.tsv"

PROCESSED_TRAINING_FILE = "/tmp/marge_processed_training_data.tsv"
PROCESSED_TESTING_FILE = "/tmp/marge_processed_testing_data.tsv"

MODEL_PATH = "/tmp/marge_model.pickle"
TESTING_PATH = "/tmp/marge_testing_data.tsv"

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

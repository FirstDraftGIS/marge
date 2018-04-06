import csv

from config import *
from datetime import datetime
from pandas import read_csv
from utils import *

start_time = datetime.now()

input_file = open(DIRTY_TESTING_FILE)
output_file = open(PROCESSED_TESTING_FILE, "w")

reader = csv.DictReader(input_file, delimiter="\t")

writer = csv.DictWriter(output_file, delimiter="\t", fieldnames=KEEPING_FOR_TESTING + NEW_FIELDS)
writer.writeheader()

count = 0
for old_row in reader:
    count += 1
    new_row = {
        "has_enwiki_title": truthify(old_row["enwiki_title"]),
        "has_population_over_1_million": has_pop_over(old_row, 1e6),
        "has_population_over_1_thousand": has_pop_over(old_row, 1e3),
        "has_population_over_1_hundred": has_pop_over(old_row, 1e2),
        #"is_place_type_b": truthify(old_row["place_type"] == "B"),
        #"is_admin": is_admin(old_row)
        #"is_country": is_country(old_row)
    }
    for key in KEEPING_FOR_TESTING:
        old_value = old_row[key]
        if old_value in ["True", "False", "true", "false"]:
            new_value = truthify(old_value)
        else:
            new_value = old_row[key]
        new_row[key] = new_value
    writer.writerow(new_row)
    if count > 1e7:
        break

input_file.close()
output_file.close()

print("finished in ", (datetime.now() - start_time).total_seconds(), "seconds")

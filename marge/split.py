from csv import DictReader
from csv import DictWriter
from random import random

from config import config

input_data_file = open(config["files"]["dirty_data_file"], encoding="utf-8")
reader = DictReader(input_data_file, delimiter="\t")
fieldnames = reader.fieldnames

training = open(config["files"]["dirty_training_file"], encoding="utf-8", mode="w")
testing = open(config["files"]["dirty_testing_file"], encoding="utf-8", mode="w")

training_writer = DictWriter(training, delimiter="\t", fieldnames=fieldnames)
training_writer.writeheader()
testing_writer = DictWriter(testing, delimiter="\t", fieldnames=fieldnames)
testing_writer.writeheader()

# iterate over groups/orders
group = []
previous_group_id = None
count = 0
for row in reader:
    count +=1

    if count % 1e5 == 0:
        print("count:", count)

    group_id = row["order_id"]
    if group_id == previous_group_id:
        group.append(row)
    else:
        if group:
            n = random() >= 0.10
            if n:
                for group_row in group:
                    training_writer.writerow(group_row)
            else:
                for group_row in group:
                    testing_writer.writerow(group_row)
        group = [row]
        previous_group_id = group_id

training.close()
testing.close()

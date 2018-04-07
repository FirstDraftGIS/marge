from csv import DictReader
from csv import DictWriter
from random import random
from config import DIRTY_DATA_FILE, DIRTY_TRAINING_FILE, DIRTY_TESTING_FILE

input_data_file = open(DIRTY_DATA_FILE)
reader = DictReader(input_data_file, delimiter="\t")
fieldnames = reader.fieldnames

training = open(DIRTY_TRAINING_FILE, "w")
testing = open(DIRTY_TESTING_FILE, "w")

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

    if count % 10000 == 0:
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

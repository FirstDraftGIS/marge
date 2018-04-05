import csv

from config import DIRTY_TRAINING_FILE, PROCESSED_TRAINING_FILE, KEEPING

input_file = open(DIRTY_TRAINING_FILE)
output_file = open(PROCESSED_TRAINING_FILE, "w")

reader = csv.DictReader(input_file)
writer = csv.DictWriter(output_file, fieldnames=KEEPING)

for old_row in reader:
    new_row = {}
    for key in KEEPING:
        old_value = old_row[key]
        if old_value in ["True", "False"]:
            new_value = "y" if old_row[key] == "True" else "n"
        else:
            new_value = old_row[key]
        new_row[key] = new_value
    writer.writerow(new_row)
    
input_file.close()
output_file.close()
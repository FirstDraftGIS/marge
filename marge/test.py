from csv import DictReader
from numpy import median
from pandas import DataFrame

from config import *
from resolver import *
from utils import *

f = open(PROCESSED_TESTING_FILE)
reader = DictReader(f, delimiter="\t")

scores = []

group = []
previous_group_id = None
for row in reader:
    #print("row:", row)
    group_id = row["order_id"]
    if group_id == previous_group_id:
        #print("group_id (", group_id, ")", "equals previous_group_id(", previous_group_id,")")
        group.append(row)
    else:
        if group:
            #print("group[0]", group[0])
            num_correct = 0
            total_number_of_features = len(set([item["feature_id"] for item in group]))
            #print("total_number_of_features:", total_number_of_features)
            options = []
            previous_feature_id = None
            for item in group:
                feature_id = item["feature_id"]
                if feature_id == previous_feature_id:
                    options.append(numerify(item))
                else:
                    if options:
                        #print("options:", options)
                        corrects = [option["correct"] for option in options]
                        #print("corrects:", set(corrects))
                        X = DataFrame.from_dict(options).drop(["order_id","feature_id","correct"], axis=1)
                        #print("X:", X)
                        selected_index = select(X)
                        #print("selected_index:", selected_index)
                        if 1.0 in corrects and selected_index == corrects.index(1.0):
                            num_correct += 1
                    options = [numerify(item)]
                    previous_feature_id = feature_id
            score = float(num_correct) / total_number_of_features
            print("score:", score)
            scores.append(score)
        group = [row]
        previous_group_id = group_id

median_score = median(scores)
print("median_score:", median_score)

f.close()

from marge.enricher import get_latest_score_key
from marge.utils import group_by


"""
When evaluating the score, we only evaluate the options that are the most
likely correct among alternatives and are likely a place


"the number of correct results divided by the number of all returned results" -
https://en.wikipedia.org/wiki/Precision_and_recall#Precision


"""


def score(test_set, model):
    
    latest_score_key = get_latest_score_key(test_set)
    
    # { "precision": _, "recall": _, "F1": _ }
    scores = []
    for order in group_by(test_set, "order_id"):
        num_incorrect = 0
        num_correct = 0
        for features in group_by(order, "feature_id"):
            #print("\n\n\nfeature_id:", feature_id)
            #pp.pprint(list(features))
            results = model.predict(list(features))
            if results is not None:
                rows = [row for row_index, row in results.iterrows()]
                if rows:
                    max_score = max([row[latest_score_key] for row in rows])
                    correct_rows = [row for row in rows if row["correct"]]
                    if correct_rows:
                        correct = correct_rows[0]
                        # do I have to worry about floating point arithmetic??
                        if correct[latest_score_key] == max_score:
                            num_correct += 1
                        else:
                            num_incorrect += 1
                    else:
                        num_incorrect += 1

        total = num_correct + num_incorrect
        if total:
            score = float(num_correct) / total
            scores.append(score)
    mean_score = mean(scores)
    return mean_score
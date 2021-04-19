"""
[entity1, relation, entity2, label] --> [entity1, relation, entity2, merged_sentence, label]
"""

import sys
sys.path.append("../")

import pandas as pd
import os
from scripts import myutils
import csv

# process train set
src_csv_path = open("./csvs/train_set - 副本.csv")
tar_csv = myutils.open_csv("processed_train_set")

tar_csv.writerow(["entity1", "relation", "entity2", "merged_sentence", "label"])

src_csv = csv.reader(src_csv_path)

for line in src_csv:
    merged_sentence = line[0].lower().strip() + " " + line[1].lower().strip() + " " + line[2].lower().strip()
    label = line[3]
    # if line[3] == "T":
    #     label = 1
    # else:
    #     label = 0
    # print(candidate_relation_triple, label)
    tar_csv.writerow([line[0], line[1], line[2], merged_sentence, label])


# process test set
src_csv_path = open("./csvs/test_set - 副本.csv")
tar_csv = myutils.open_csv("processed_test_set")

tar_csv.writerow(["entity1", "relation", "entity2", "merged_sentence", "label"])

src_csv = csv.reader(src_csv_path)

for line in src_csv:
    merged_sentence = line[0].lower().strip() + " " + line[1].lower().strip() + " " + line[2].lower().strip()
    label = line[3]
    # if line[3] == "T":
    #     label = 1
    # else:
    #     label = 0
    # print(candidate_relation_triple, label)
    tar_csv.writerow([line[0], line[1], line[2], merged_sentence, label])


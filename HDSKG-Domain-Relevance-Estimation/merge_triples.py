"""
[entity1, relation, entity2, label] --> [entity1, relation, entity2, merged_sentence, label]
"""

import sys
sys.path.append("../")

import pandas as pd
import os
from scripts import myutils
import csv
from tqdm import tqdm

# process train set
src_csv_path = open("../csvs/manual_labeled_train_set.csv")
tar_csv = myutils.open_csv("processed_train_set")

tar_csv.writerow(["entity1", "relation", "entity2", "merged_sentence", "label"])

src_csv = csv.reader(src_csv_path)

print("..........process manual labelled train set..........")
for line in tqdm(src_csv):
    merged_sentence = line[0].lower().strip() + " " + line[1].lower().strip() + " " + line[2].lower().strip()
    label = line[3]
    tar_csv.writerow([line[0], line[1], line[2], merged_sentence, label])


# process test set
src_csv_path = open("../csvs/manual_labeled_test_set.csv")
tar_csv = myutils.open_csv("processed_test_set")

tar_csv.writerow(["entity1", "relation", "entity2", "merged_sentence", "label"])

src_csv = csv.reader(src_csv_path)

print("..........process manual labelled test set..........")
for line in tqdm(src_csv):
    merged_sentence = line[0].lower().strip() + " " + line[1].lower().strip() + " " + line[2].lower().strip()
    label = line[3]
    tar_csv.writerow([line[0], line[1], line[2], merged_sentence, label])


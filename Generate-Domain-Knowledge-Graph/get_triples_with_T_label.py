"""
get all relation triples with T label
input: the path of labeled csv
output: the csv file contains all triples with T labels
"""

import sys
sys.path.append("../")

import csv
from tqdm import tqdm
from scripts import myutils

def get_triples_with_T_label(labeled_csv_path):
    T_labeled_triples = myutils.open_csv("T_labeled_triples")
    with open(labeled_csv_path, newline='', encoding="gb18030") as src_csv_path:
        src_csv = csv.reader(src_csv_path)
        for line in tqdm(src_csv):
            # print(line)
            if line[4] == "T":
                T_labeled_triples.writerow([line[0], line[1], line[2]])





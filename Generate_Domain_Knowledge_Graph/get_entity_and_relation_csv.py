"""
"""
import sys
sys.path.append("../")

import csv
from tqdm import tqdm
from scripts import myutils

def get_entity_and_relation_csv(T_labeled_triples_path):
    entities = set()
    entities_ID_dict = dict()
    entities_cnt = 0

    entity_csv = myutils.open_csv("entity_csv")
    entity_csv.writerow(["entity:ID", "name"])

    relation_csv = myutils.open_csv("relation_csv")
    relation_csv.writerow([":START_ID", ":END_ID", ":TYPE"])

    with open(T_labeled_triples_path, newline='') as src_csv_path:
        src_csv = csv.reader(src_csv_path)
        for line in src_csv:
            head_entity = line[0]
            tail_entity = line[2]
            # duplicate removal, set an unique ID for every entity
            if head_entity not in entities:
                entities.add(head_entity)
                head_entity_ID = "entity_" + str(entities_cnt)
                entities_ID_dict[head_entity] = head_entity_ID
                entity_csv.writerow([head_entity_ID, head_entity])
                entities_cnt += 1
            else:
                head_entity_ID = entities_ID_dict[head_entity]

            if tail_entity not in entities:
                entities.add(tail_entity)
                tail_entity_ID = "entity_" + str(entities_cnt)
                entities_ID_dict[tail_entity] = tail_entity_ID
                entity_csv.writerow([tail_entity_ID, tail_entity])
                entities_cnt += 1
            else:
                tail_entity_ID = entities_ID_dict[tail_entity]

            # generate relation_csv, [:START_ID, :END_ID, :TYPE] -> [head_entity_ID, tail_entity_ID, relation]
            relation_csv.writerow([head_entity_ID, tail_entity_ID, line[1]])


get_entity_and_relation_csv("../csvs/T_labeled_triples.csv")
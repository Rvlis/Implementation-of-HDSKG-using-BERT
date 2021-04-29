"""
"""
import sys
import os
sys.path.append("../")

import csv
from tqdm import tqdm
from scripts import myutils

def get_triples_with_T_label(labeled_csv_path):
    """
    get all relation triples with T label

    :param labeled_csv_path: the path of labeled csv
    get the csv file contains all triples with T labels
    """

    print("----------get triples with T label----------")
    T_labeled_triples = myutils.open_csv("T_labeled_triples")
    with open(labeled_csv_path, newline='', encoding="gb18030") as src_csv_path:
        src_csv = csv.reader(src_csv_path)
        for line in tqdm(src_csv):
            # print(line)
            try:
                if line[4] == "T":
                    T_labeled_triples.writerow([line[0], line[1], line[2]])
            except:
                pass

def get_entity_and_relation_csv(T_labeled_triples_path):
    """
    get entity.csv and relation.csv used for generate knowledge graph with neo4j

    :param T_labeled_triples_path: get_triples_with_T_label's output path

    get entity.csv and relation.csv
    """

    get_triples_with_T_label("../csvs/labeled_relation_triples.csv")

    # get all clusters: 6 type
    relation_type = dict()
    for i in range(6):
        with open("../data/new-cluster-"+str(i)+".txt", "r") as rf:
            VPs = rf.readlines()
            for VP in VPs:
                relation_type[VP.strip()] = i
    print(relation_type)
    os.system("pause")
    print("----------get entity and relation csv----------")

    entities = set()
    entities_ID_dict = dict()
    entities_cnt = 0
    # guarantee geted triple is unique
    triples_set = set()

    entity_csv = myutils.open_csv("entity_csv")
    entity_csv.writerow(["entity:ID", "name"])

    relation_csv = myutils.open_csv("relation_csv")
    relation_csv.writerow([":START_ID", ":END_ID", ":TYPE"])

    with open(T_labeled_triples_path, newline='', encoding="gb18030") as src_csv_path:
        src_csv = csv.reader(src_csv_path)
        for line in tqdm(src_csv):
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
            if (head_entity_ID, tail_entity_ID, line[1]) not in triples_set:
                relation_csv.writerow([head_entity_ID, tail_entity_ID, "relation_type_"+str(relation_type[line[1].strip()])])
                triples_set.add((head_entity_ID, tail_entity_ID, "relation_type_"+str(relation_type[line[1].strip()])))




# get_entity_and_relation_csv("../csvs/T_labeled_triples.csv")

get_entity_and_relation_csv("../csvs/T_labeled_triples.csv")

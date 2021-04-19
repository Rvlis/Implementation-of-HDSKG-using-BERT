# import sys
# sys.path.append("../")

# # import spacy
# # import neuralcoref

# # nlp = spacy.load("en_core_web_md")
# # neuralcoref.add_to_pipe(nlp)

# # doc = nlp(u'Cython is an optimising static compiler for both the Python programming language and the extended Cython programming language (based on Pyrex). It makes writing C extensions for Python as easy as Python itself.')

# # print(doc._.has_coref)
# # print(doc._.coref_clusters)
# # print(doc._.coref_resolved)
# import pandas as pd
# import os
# from scripts import myutils
# import csv

# # process train set
# src_csv_path = open("./csvs/train_set - 副本.csv")
# tar_csv = myutils.open_csv("processed_train_set")

# tar_csv.writerow(["candidate_relation_triple", "label"])

# src_csv = csv.reader(src_csv_path)

# for line in src_csv:
#     candidate_relation_triple = line[0].lower().strip() + " " + line[1].lower().strip() + " " + line[2].lower().strip()
#     if line[3] == "T":
#         label = 1
#     else:
#         label = 0
#     # print(candidate_relation_triple, label)
#     tar_csv.writerow([candidate_relation_triple, label])


# # process test set
# src_csv_path = open("./csvs/test_set - 副本.csv")
# tar_csv = myutils.open_csv("processed_test_set")

# tar_csv.writerow(["candidate_relation_triple", "label"])

# src_csv = csv.reader(src_csv_path)

# for line in src_csv:
#     candidate_relation_triple = line[0].lower().strip() + " " + line[1].lower().strip() + " " + line[2].lower().strip()
#     if line[3] == "T":
#         label = 1
#     else:
#         label = 0
#     # print(candidate_relation_triple, label)
#     tar_csv.writerow([candidate_relation_triple, label])


import stanza

stanza.install_corenlp("D:\Aaasoft\coreNLP")
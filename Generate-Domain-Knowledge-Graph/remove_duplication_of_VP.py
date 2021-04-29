"""
duplicate removal, get unique VP
"""

with open("./data/VP.txt", 'r') as cf:
        docs = cf.readlines()
        print(len(docs))

phrases_set = set()
for doc in docs:
    phrases_set.add(doc)
phrases = list(phrases_set)
with open("./data/VP.txt", "w") as wf:
    for phrase in phrases:
        # print(phrase)
        wf.write(phrase)
    print(len(phrases))
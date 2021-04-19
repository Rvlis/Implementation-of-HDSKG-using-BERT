"""
implementation of Ⅲ. APPROACH B. Pre-process Text 共指消解
spacy=2.3.2
neuralcoref=4.0 
"""
import sys
sys.path.append("../")

import spacy
import neuralcoref
from tqdm import tqdm

import data_spider # spider data from webpage
from scripts import myutils

nlp = spacy.load("en_core_web_md")
neuralcoref.add_to_pipe(nlp)

def pre_process_text():

    input_sentences = list()

    contents = data_spider.data_spider()

    myutils.remove_file("../csvs/input_sentence.csv")
    input_sentences_csv = myutils.open_csv("input_sentence","a")

    print("----------Preprocessing text----------")
    for content in tqdm(contents):
        doc = nlp(content)
        # print(type(doc._.coref_resolved))
        doc = nlp(doc._.coref_resolved)
        for sentence in doc.sents:
            sentence = str(sentence).replace("\n"," ").replace("\t"," ")
            if len(sentence) <= 50:
                continue
            input_sentences.append(sentence)
            input_sentences_csv.writerow([sentence])
    return input_sentences

# pre_process_text()

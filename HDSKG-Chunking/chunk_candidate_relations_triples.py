"""
It has been deprecated.
This is a module using spacy instead of coreNLP.
-> See corenlp_chunk_candidate_relations_triples.py
"""
from bs4 import BeautifulSoup
import shutil
import re
import os
import csv
import sys
from tqdm import tqdm
import nltk
from nltk.tokenize import sent_tokenize
from nltk.parse.stanford import StanfordDependencyParser
import numpy as np
import spacy
from spacy.matcher import Matcher
from spacy import displacy


eng_parser = StanfordDependencyParser(r"D:\Chrome\Dl\stanford-parser-full-2016-10-31\stanford-parser.jar",
r"D:\Chrome\Dl\stanford-parser-full-2016-10-31\stanford-parser-3.7.0-models.jar",
r"D:\Chrome\Dl\stanford-parser-full-2016-10-31\edu\stanford\nlp\models\lexparser\englishPCFG.ser.gz")

nlp = spacy.load("en_core_web_md")

# 定义匹配模式
VVP_patterns = [
    [{"TAG":"MD","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"?"}, {"POS":"DET","OP":"?"}, {"POS":"PART","OP":"+"}, {"POS":"VERB","OP":"+"}],
    [{"TAG":"MD","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"?"}, {"POS":"DET","OP":"?"}, {"POS":"ADP","OP":"+"}, {"POS":"VERB","OP":"+"}],
    [{"POS":"AUX","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"?"}, {"POS":"DET","OP":"?"}, {"POS":"PART","OP":"+"}, {"POS":"VERB","OP":"+"}],
    [{"POS":"AUX","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"?"}, {"POS":"DET","OP":"?"}, {"POS":"ADP","OP":"+"}, {"POS":"VERB","OP":"+"}]
]

VP_patterns = [
    [{"TAG":"MD","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"NUM","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"?"}, {"POS":"DET","OP":"?"}, {"POS":"ADP","OP":"+"}],
    [{"TAG":"MD","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"NUM","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"?"}, {"POS":"DET","OP":"?"}, {"POS":"PART","OP":"+"}],
    [{"TAG":"MD","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"?"}, {"POS":"DET","OP":"?"}, {"POS":"ADP","OP":"+"}],
    [{"TAG":"MD","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"?"}, {"POS":"DET","OP":"?"}, {"POS":"PART","OP":"+"}],
    [{"TAG":"MD","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"+"}],
    [{"TAG":"MD","OP":"*"}, {"POS":"VERB","OP":"+"}],
    [{"POS":"AUX","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"NUM","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"?"}, {"POS":"DET","OP":"?"}, {"POS":"ADP","OP":"+"}],
    [{"POS":"AUX","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"NUM","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"?"}, {"POS":"DET","OP":"?"}, {"POS":"PART","OP":"+"}],
    [{"POS":"AUX","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"?"}, {"POS":"DET","OP":"?"}, {"POS":"ADP","OP":"+"}],
    [{"POS":"AUX","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"?"}, {"POS":"DET","OP":"?"}, {"POS":"PART","OP":"+"}],
    [{"POS":"AUX","OP":"*"}, {"POS":"VERB","OP":"+"}, {"POS":"ADJ","OP":"*"}, {"POS":"ADV","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"VERB","OP":"+"}],
    [{"POS":"AUX","OP":"*"}, {"POS":"VERB","OP":"+"}]
]

NP_patterns = [
    [{"POS":"NUM","OP":"*"}, {"POS":"DET","OP":"?"}, {"POS":"NUM","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"NUM","OP":"*"}, {"TAG":"VBD","OP":"*"}, {"TAG":"VBG","OP":"*"}, {"POS":"NOUN","OP":"*"}, {"POS":"PROPN","OP":"*"}, {"POS":"PART","OP":"*"}, {"POS":"NUM","OP":"*"}, {"TAG":"VBD","OP":"*"}, {"TAG":"VBG","OP":"*"}, {"POS":"NOUN","OP":"*"}, {"POS":"PROPN","OP":"*"}, {"TAG":"VBD","OP":"*"}, {"TAG":"VBG","OP":"*"}, {"POS":"NOUN","OP":"*"}, {"POS":"PROPN","OP":"*"}, {"POS":"PART","OP":"*"}, {"POS":"NUM","OP":"*"}, {"POS":"NOUN","OP":"+"}],
    [{"POS":"NUM","OP":"*"}, {"POS":"DET","OP":"?"}, {"POS":"NUM","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"NUM","OP":"*"}, {"TAG":"VBD","OP":"*"}, {"TAG":"VBG","OP":"*"}, {"POS":"NOUN","OP":"*"}, {"POS":"PROPN","OP":"*"}, {"POS":"PART","OP":"*"}, {"POS":"NUM","OP":"*"}, {"TAG":"VBD","OP":"*"}, {"TAG":"VBG","OP":"*"}, {"POS":"NOUN","OP":"*"}, {"POS":"PROPN","OP":"*"}, {"TAG":"VBD","OP":"*"}, {"TAG":"VBG","OP":"*"}, {"POS":"NOUN","OP":"*"}, {"POS":"PROPN","OP":"*"}, {"POS":"PART","OP":"*"}, {"POS":"NUM","OP":"*"}, {"POS":"PROPN","OP":"+"}]
    # [{"POS":"NUM","OP":"*"}, {"POS":"DET","OP":"?"}, {"POS":"NUM","OP":"*"}, {"POS":"ADJ","OP":"*"}, {"POS":"NUM","OP":"*"}, {"POS":"VERB","OP":"*"}, {"POS": NN,"OP":"*"}, {"POS":"PART","OP":"*"}, {"POS":"NUM","OP":"*"}, {"POS":"VERB","OP":"*"}, {"POS":NN,"OP":"*"}, {"POS":"VERB","OP":"*"}, {"POS":NN,"OP":"*"}, {"POS":"PART","OP":"*"}, {"POS":"NUM","OP":"*"}, {"POS":NN,"OP":"+"}]  for NN in ["NOUN", "PROPN"]
]

matcher = Matcher(nlp.vocab)
# 添加匹配模式
matcher.add("VVP_patterns", VVP_patterns, greedy="LONGEST")
matcher.add("VP_patterns", VP_patterns, greedy="LONGEST")
matcher.add("NP_patterns", NP_patterns, greedy="LONGEST")

candidate_relations_triples = list()

def chunk_NP_and_VP_by_ruled_based_chunking(sentence):
    """
    """
    doc = nlp(sentence)
    NP = list()
    VP = list()
    # for token in doc:
    #     print(token, token.pos_)
    matches = matcher(doc)
    for match_id, start, end in matches:
        pattern_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        # print(pattern_id,"->",span.text)

        # [start,end] NP/VP
        if str(pattern_id) == "NP_patterns" :
            NP.append([[start,end],span.text])
        elif str(pattern_id) == "VP_patterns" or str(pattern_id) == "VVP_patterns":
            VP.append([[start,end],span.text])
    
    return NP,VP



def dependency_parsing(sentence):
    """
    """
    NP, VP = chunk_NP_and_VP_by_ruled_based_chunking(sentence)
    # print(NP, VP)
    doc = nlp(sentence)

    # Scenario 1
    for np in NP:
        start,end = np[0]
        # print(start, end)
        for pos in range(start,end):
            token = doc[pos]
            dep = token.dep_

            # 文中定义nsubjpass(n12,v13),额外添加 nsubj()
            if dep == "nsubjpass" or dep == "nsubj":
                # print(token.head.text, token.head.i)
                np1 = np[1]
                i = token.head.i
                token_vp = token.head.text
                # 找到token.head所属的vp
                for vp in VP:
                    start,end = vp[0]
                    if i >= start and i <= end:
                        span_vp = vp[1]
                        # print("span_vp:",vp)
                        break
                # print("np1:",np1)
                # print("vp1:",vp1)

                # 文中定义dobj(v13, n22)
                for np in NP:
                    start,end = np[0]
                    for pos in range(start,end):
                        token1 = doc[pos]
                        dep = token1.dep_
                        # 注意判断跟 vp 比较而不是vp1，因为vp属于token，vp1 属于span
                        if token1.head.text == token_vp and dep == "dobj":
                            np2 = np[1]
                            print([np1,span_vp,np2])
                            candidate_relations_triples.append([np1,span_vp,np2])
                        # Scenario 4:判断在两个NP之间是否存在and关系
                            for np in NP:
                                start,end = np[0]
                                for pos in range(start,end):
                                    token2 = doc[pos]
                                    dep = token2.dep_
                                    if token2.head.text == token1.text and dep == "conj":
                                        np3 = np[1]
                                        print([np1,span_vp,np3])
                                        candidate_relations_triples.append([np1,span_vp,np3])
    
    # Scenario 2
    # Scenario 3
    # Scenario 4
    # for np in NP:
    #     start,end = np[0]
    #     # print(start, end)
    #     for pos in range(start,end):
    #         token = doc[pos]
    #         dep = token.dep_

    #         # 文中定义nsubjpass(n12,v13),额外添加 nsubj()
    #         if dep == "nsubjpass" or dep == "nsubj":
    #             np1 = np[1]

    #             i = token.head.i
    #             # token_vp:token
    #             token_vp = token.head.text
    #             # 找到token.head所属的vp
    #             for vp in VP:
    #                 start,end = vp[0]
    #                 if i >= start and i <= end:
    #                     # vp1：span
    #                     span_vp = vp[1]
    #                     break
                
    #             for np in NP:
    #                 start,end = np[0]
    #                 for pos in range(start,end):
    #                     token1 = doc[pos]
    #                     dep = token1.dep_
    #                     # 注意判断跟 vp 比较而不是vp1，因为vp属于token，vp1 属于span
    #                     if token1.head.text == token_vp and dep == "dobj":
    #                         np2 = np[1]
    #                         print([np1,span_vp,np2])
    #                         candidate_relations_triples.append([np1,span_vp,np2])
    #                     # 判断在两个NP之间是否存在and关系
    #                         for np in NP:
    #                             start,end = np[0]
    #                             for pos in range(start,end):
    #                                 token2 = doc[pos]
    #                                 dep = token2.dep_
    #                                 if token2.head.text == token1.text and dep == "conj":
    #                                     np3 = np[1]
    #                                     print([np1,span_vp,np3])
    #                                     candidate_relations_triples.append([np1,span_vp,np3])

    # Scenario 5
    for vp in VP:
        start,end = vp[0]
        for pos in range(start,end):
            token = doc[pos]
            dep = token.dep_

            if dep == "xcomp" or dep == "advcl":
                token_vp1 = token
                # 文中token_vp2：ROOT
                token_vp2 = token.head.text
                i = token.head.i
                span_vp1 = vp[1]
                # 找到span_vp2
                for vp in VP:
                    start,end = vp[0]
                    if i >= start and i <= end:
                        span_vp2 = vp[1]
                        break
                # print(token_vp1, token_vp2)
                # print(span_vp1, span_vp2)
                for np in NP:
                    start,end = np[0]
                    for pos in range(start,end):
                        np_token = doc[pos]
                        dep = np_token.dep_
                        # if dep == "nsubjpass" or dep == "nsubj":
                            # print("np_token:",np_token)
                





    # Scenario 6
    


    # displacy.render(doc, style="dep")
    displacy.serve(doc, style="dep")

    # print(spacy.explain(u"nmod"))

    # spacy
    for token in doc:
         print("{0}({1}) -- {2} --> {3}({4})".format(token.head.text, token.head.pos_, token.dep_, token.text, token.pos_))
    res = list(eng_parser.parse(sentence.split()))

    # nltk
    # print("--------------------------------------------------------------------")
    # for row in res[0].triples():
    #     print(row)



sentence0 = "PyTables is built on top of the HDF5 library, using the Python language and the NumPy package."
# sentence1 = "OpenRPT provides WYSIWYG editor"
# sentence2 = "HSQLDB is supported by many Java frameworks. "
# sentence3 = "flashcanvas renders shapes and images."

sentences = [sentence0]

# NP, VP = chunk_NP_and_VP_by_ruled_based_chunking(sentence)
# print(NP, VP)
for sentence in sentences:
    dependency_parsing(sentence)

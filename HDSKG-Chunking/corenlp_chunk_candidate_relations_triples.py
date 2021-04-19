"""
implementation of paper "HDSKG" : (Ⅲ.) APPROACH  part D. "Chunk Candidate Relations Triples"
"""
import sys
sys.path.append("../")

from stanza.server import CoreNLPClient
import os
from tqdm import tqdm
import scenarios        # implementation of 6 scenarios
import pre_process_text # implementation of preprocess text
from scripts import myutils


# Table Ⅰ. REGULAR EXPRESSION OF DIFFERENT CHUNKS
VVP_pattern = [
    # (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(TO*)+(VB)+
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:TO]{1,})([pos:VB]{1,})",
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:IN]{1,})([pos:VBG]{1,})"
]

VP_pattern = [
    # (MD)*(VB.*)+(CD)*(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(IN*|TO*)+
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:CD]*)([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:/IN|TO/]{1,})",
    # (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(IN*|TO*)+
    # "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]?)([pos:DT]?)([pos:/IN|TO/]{1,})",
    # (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)+
    "([pos:MD]*)([pos:/VB.*/]{1,})([pos:JJ]*)([pos:RB]*)([pos:JJ]*)([pos:/VB.*/]{1,})",
    # (MD)*(VB.*)+
    "([pos:MD]*)([pos:/VB.*/]{1,})"
]

NP_pattern = [
    # (CD)*(DT)?(CD)*(JJ)*(CD)*(VBD|VBG)*(NN.*)*-
    # (POS)*(CD)*(VBD|VBG)*(NN.*)*-
    # (VBD|VBG)*(NN.*)*(POS)*(CD)*(NN.*)+
    "([pos:CD]*)([pos:DT]?)([pos:CD]*)([pos:JJ]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:/VBD|VBG/]*)([pos:/NN.*/]*)([pos:POS]*)([pos:CD]*)([pos:/NN.*/]{1,})"
]



def chunk_candidate_relations_triples(input_sentences):
    """
    implementation of (Ⅲ.) APPROACH  part D. "Chunk Candidate Relations Triples"
    :param input_sentences: list[input_sentence1, input_sentence2, ...]

    """
    candidate_relations_triples = list()
    # set up the client
    with CoreNLPClient(annotators=['tokenize','ssplit','pos','depparse'], timeout=60000, memory='4G', be_quiet=True) as client:

        print("----------chunk candidate relations triples----------")
        for input_sentence in tqdm(input_sentences):
            # print(input_sentence)
            ann = client.annotate(input_sentence)
            sentence = ann.sentence[0]

            # HDSKG's method
            # denpendency_rel: source, target, dep
            dependency_rel = list()
            enhanced_plus_plus_dependency_parse = sentence.enhancedPlusPlusDependencies
            edges = list(enhanced_plus_plus_dependency_parse.edge)
            for edge in edges:
                # print(type(edge.source),type(edge.target),type(edge.dep))
                dependency_rel.append([edge.source-1, edge.target-1, edge.dep])
            # print(list(enhanced_plus_plus_dependency_parse.edge))
            # for item in dependency_rel:
            #     print(item)
            # os.system("pause")

            VPs = list()
            NPs = list()

            # VVP_pattern
            for pattern in VVP_pattern:
                matches = client.tokensregex(input_sentence, pattern)
                # length means the number of matched phrase
                length = matches["sentences"][0]["length"]
                if length != 0:
                    for i in range(length):
                        text = matches["sentences"][0][str(i)]["text"]
                        begin = matches["sentences"][0][str(i)]["begin"]
                        end = matches["sentences"][0][str(i)]["end"]
                        # print(matches["sentences"][0][str(i)]["text"], matches["sentences"][0][str(i)]["begin"], matches["sentences"][0][str(i)]["end"])
                        VPs.append([text,begin,end])

            # VP_pattern
            for pattern in VP_pattern: 
                matches = client.tokensregex(input_sentence, pattern)
                # print(matches)
                # length means the number of matched phrase
                length = matches["sentences"][0]["length"]
                if length != 0:
                    for i in range(length):
                        text = matches["sentences"][0][str(i)]["text"]
                        begin = matches["sentences"][0][str(i)]["begin"]
                        end = matches["sentences"][0][str(i)]["end"]
                        # print(matches["sentences"][0][str(i)]["text"], matches["sentences"][0][str(i)]["begin"], matches["sentences"][0][str(i)]["end"])
                        # VP存在重复匹配问题，需要多加一步判断
                        flag = True
                        for item in VPs:
                            if begin >= item[1] and end <= item[2]:
                                flag = False
                                break
                        if flag:
                            VPs.append([text,begin,end])

            # NP_pattern
            for pattern in NP_pattern:
                matches = client.tokensregex(input_sentence, pattern)
                # print(matches)
                # length means the number of matched phrase
                length = matches["sentences"][0]["length"]
                if length != 0:
                    for i in range(length):
                        text = matches["sentences"][0][str(i)]["text"]
                        begin = matches["sentences"][0][str(i)]["begin"]
                        end = matches["sentences"][0][str(i)]["end"]
                        # print(matches["sentences"][0][str(i)]["text"], matches["sentences"][0][str(i)]["begin"], matches["sentences"][0][str(i)]["end"])
                        NPs.append([text,begin,end])

            # for item in VPs:
            #     print(item[0],item[1],item[2])
            # for item in NPs:
            #     print(item[0],item[1],item[2])

            candidate_relations_triples.extend(scenarios.Scenario(dependency_rel, VPs, NPs))
            
    # for item in candidate_relations_triples:
    #     print(item)

    # myutils.remove_file("./csvs/candidate_relation_triples.csv")
    crt_csv = myutils.open_csv("candidate_relation_triples", "a")
    for item in candidate_relations_triples:
        # print(item)
        crt_csv.writerow(
            [item[1], item[2], item[3]]
        )
    
    
            

# input_sentences = [
#     "PyTables is built on top of the HDF5 library, using the Python language and the NumPy package.",
#     "OpenRPT provides WYSIWYG editor",
#     "HSQLDB is supported by many Java frameworks.",
#     "webkit is developed by Intel at the Intel Open Source Technology Center.",
#     "flashcanvas renders shapes and images.",
#     "Joone is used to build neural networks.",
#     "Firebird is written in C++, and is ultimately derived from the Borland InterBase 6.0 source code.",
#     "Eclipse on your system can be used as a Java editor."
# ]

input_sentences = pre_process_text.pre_process_text()
# print(input_sentences)

chunk_candidate_relations_triples(input_sentences)

"""
Implementation 6 scenarios, I noticed that some scen are similarly, such as 1 and 4, 2 and 3.
So there are less than 6 scenarios's detailed code. 
"""

def is_nsubjpass(source, target, vp, np):
    """
    :param source: int, dep_edge's source node
    :param target: int, dep_edge's target node
    :param vp: list[text, start, end], source maybe in text
    :param np: list[], target maybe in text

    :return true|false
    """
    # pass
    if source >= vp[1] and source < vp[2]:
        if target >= np[1] and target < np[2]:
            return True
    return False


def is_dobj(source, target, vp, np):
    # pass
    if source >= vp[1] and source < vp[2]:
        if target >= np[1] and target < np[2]:
            return True
    return False


def is_nmod_or_obl(source, target, vp, np):
    # pass
    if source >= vp[1] and source < vp[2]:
        if target >= np[1] and target < np[2]:
            return True
    return False


def is_dep_or_xcomp(source, target, vp1, vp2):
    # pass
    if source >= vp1[1] and source < vp1[2]:
        if target >= vp2[1] and target < vp2[2]:
            return True
    return False

# S.4 can also be implemented by this func.
def Scenario_1(dependency_rel, VPs, NPs):
    """
    :param dependency_rel: list[source_index, target_index, dependency]
    :param VPs: list[text, start, end], VP by rule-based chunking
    :param NPs: list[text, start, end], NP by rule-based chunking

    :return cadidate_relations_triples: list[VP, NP, VP]
    """

    candidate_relations_triples = list()
    
    # s.1 includes two dependencise: nsubj and dobj
    nsubjpass = [item for item in dependency_rel if item[2] == "nsubj:pass" or item[2] == "nsubj"] 
    dobj = [item for item in dependency_rel if item[2] == "dobj" or item[2] == "obj"]

    for n_item in nsubjpass:
        n_source = n_item[0]
        n_target = n_item[1]
        for vp in VPs:
                for np_1 in NPs:
                    if is_nsubjpass(n_source, n_target, vp, np_1):
                        for d_item in dobj:
                            d_source = d_item[0]
                            d_target = d_item[1]
                            for np_2 in NPs:
                                if d_source == n_source and is_dobj(d_source, d_target, vp, np_2):
                                    candidate_relations_triples.append(["S1",np_1[0],vp[0],np_2[0]]) 
    # print("nsubjpass is ",nsubjpass)
    # for n_item in nsubjpass:
    #     n_source = n_item[0]
    #     n_target = n_item[1]
    #     for vp in VPs:
    #         if n_source >= vp[1] and n_source < vp[2]:
    #             for np_1 in NPs:
    #                 if n_target >= np_1[1] and n_target < np_1[2]:
    #                     for d_item in dobj:
    #                         d_source = d_item[0]
    #                         d_target = d_item[1]
    #                         if d_source >= vp[1] and d_source < vp[2]:
    #                             for np_2 in NPs:
    #                                 if d_target >= np_2[1] and d_target < np_2[2]:
    #                                     candidate_relations_triples.append([np_1[0],vp[0],np_2[0]])

    # print(candidate_relations_triples)
    return candidate_relations_triples


def Scenario_2(dependency_rel, VPs, NPs):
    """
    todo:
        Notice that with the preposition of dependency “nmod:at”, 
        the preposition of VP1 “is_developed_by” can be changed to “at” while chunking the second relation triples.
    """
    candidate_relations_triples = list()

    # two dependicies: nsubj and nmod or obl
    nsubjpass = [item for item in dependency_rel if item[2] == "nsubj:pass" or item[2] == "nsubj"] 
    nmod_obl = [item for item in dependency_rel if item[2].find("nmod") != -1 or item[2].find("obl") != -1]

    for n_item in nsubjpass:
        n_source = n_item[0]
        n_target = n_item[1]
        for vp in VPs:
                for np_1 in NPs:
                    if is_nsubjpass(n_source, n_target, vp, np_1):
                        for d_item in nmod_obl:
                            d_source = d_item[0]
                            d_target = d_item[1]
                            for np_2 in NPs:
                                if d_source == n_source and is_dobj(d_source, d_target, vp, np_2):
                                    candidate_relations_triples.append(["S2",np_1[0],vp[0],np_2[0]]) 

    # print(candidate_relations_triples)
    return candidate_relations_triples

def Scenario_3(dependency_rel, VPs, NPs):
    pass
    # can be implemented by S2

    # candidate_relations_triples = list()

    # nsubjpass = [item for item in dependency_rel if item[2] == "nsubj:pass" or item[2] == "nsubj"] 
    # nmod_obl = [item for item in dependency_rel if item[2].find("nmod") != -1 or item[2].find("obl") != -1]

    # for n_item in nsubjpass:
    #     n_source = n_item[0]
    #     n_target = n_item[1]
    #     for vp in VPs:
    #             for np_1 in NPs:
    #                 if is_nsubjpass(n_source, n_target, vp, np_1):
    #                     for d_item in nmod_obl:
    #                         d_source = d_item[0]
    #                         d_target = d_item[1]
    #                         for np_2 in NPs:
    #                             if is_dobj(d_source, d_target, vp, np_2):
    #                                 candidate_relations_triples.append([np_1[0],vp[0],np_2[0]]) 

    # # print(candidate_relations_triples)
    # return candidate_relations_triples

def Scenario_4(dependency_rel, VPs, NPs):
    # can be implemented by S.1
    pass

def Scenario_5(dependency_rel, VPs, NPs):

    candidate_relations_triples = list()
    candidate_relations_triples.extend(Scenario_2(dependency_rel, VPs, NPs))

    nsubjpass = [item for item in dependency_rel if item[2] == "nsubj:pass" or item[2] == "nsubj"] 
    dep_xcomp = [item for item in dependency_rel if item[2] == "dep" or item[2] == "xcomp"]
    dobj = [item for item in dependency_rel if item[2] == "dobj" or item[2] == "obj"]

    for n_item in nsubjpass:
        n_source = n_item[0]
        n_target = n_item[1]
        for vp_1 in VPs:
                for np_1 in NPs:
                    if is_nsubjpass(n_source, n_target, vp_1, np_1):
                        for d_item in dep_xcomp:
                            d_source = d_item[0]
                            d_target = d_item[1]
                            for vp_2 in VPs:
                                if is_dep_or_xcomp(d_source, d_target, vp_1, vp_2):
                                    # candidate_relations_triples.append([np_1[0],vp[0],np_2[0]]) 
                                    for dobj_item in dobj:
                                        dobj_source = dobj_item[0]
                                        dobj_target = dobj_item[1]
                                        for np_2 in NPs:
                                            if d_target == dobj_source and is_dobj(dobj_source, dobj_target, vp_2, np_2):
                                                candidate_relations_triples.append(["S5",np_1[0], vp_2[0], np_2[0]])


    # print(candidate_relations_triples)
    return candidate_relations_triples

def Scenario(dependency_rel, VPs, NPs):
    # all scenarios
    candidate_relations_triples = list()
    candidate_relations_triples.extend(Scenario_1(dependency_rel, VPs, NPs))
    # candidate_relations_triples.extend(Scenario_3(dependency_rel, VPs, NPs))
    candidate_relations_triples.extend(Scenario_5(dependency_rel, VPs, NPs))
    
    return candidate_relations_triples
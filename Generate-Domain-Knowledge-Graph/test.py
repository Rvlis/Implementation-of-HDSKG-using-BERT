import sys
import os
import shutil
import gensim
import numpy as np
 
from gensim.models.doc2vec import Doc2Vec, LabeledSentence
from sklearn.cluster import KMeans
 
from gensim.models.doc2vec import TaggedDocument
 
def get_datasest():

    with open("../csvs/unique_VP.txt", "r") as rf:
        docs = rf.readlines()
        print(len(docs))

    x_train = []
    for i, text in enumerate(docs):
        text = text.strip()
        word_list = text.split(' ')
        document = TaggedDocument(word_list, tags=[i])
        x_train.append(document)
 
    return x_train
 
def train(x_train, size=200, epoch_num=1):
    model_dm = Doc2Vec(x_train,min_count=1, window = 3, size = size, sample=1e-3, negative=5, workers=4)
    model_dm.train(x_train, total_examples=model_dm.corpus_count, epochs=100)
    model_dm.save('../model/model_dm')
 
    return model_dm
 
def cluster(x_train):
    infered_vectors_list = []
    print("load doc2vec model...")
    model_dm = Doc2Vec.load("../model/model_dm")
    print("load train vectors...") 
    i = 0
    for text, label in x_train:
        vector = model_dm.infer_vector(text)
        infered_vectors_list.append(vector)
        i += 1
 
    print("train kmean model...")
    kmean_model = KMeans(n_clusters=8, n_jobs=-1)
    kmean_model.fit(infered_vectors_list)
    labels = kmean_model.labels_
    cluster_centers = kmean_model.cluster_centers_


    try:
        shutil.rmtree("../data/")
        os.mkdir("../data/")
    except:
        pass
    # os.system("pause")

    for i in range(len(x_train)):
        text = x_train[i][0]
        sentence = ""
        for word in text:
            sentence = sentence + word + " "
        sentence = sentence.strip()
        with open("../data/new-cluster-"+str(labels[i])+".txt", "a") as wf:
            wf.write(sentence+"\n")

    return cluster_centers
 
 
 
 
x_train = get_datasest()
model_dm = train(x_train)
cluster_centers = cluster(x_train)
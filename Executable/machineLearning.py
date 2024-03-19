from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import spacy
import os
import random
import pickle

nlp = spacy.load("en_core_web_sm") # Loading Spacy's English module

class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if name == 'customTokenizer':
            from SVMabstractClassifier import customTokenizer
            return customTokenizer
        return super().find_class(module, name)

def np_to_fs(og_dict):
    for k, v in og_dict.items():
        if type(v).__module__ == 'numpy':
            og_dict[k] = v.item() # Converts numpy variables to regular python variables

def add_category(progress_bar, data, root):
    progress_bar['value'] = 0
    root.update()
    total_dicts = len(data)

    with open('svm_classifier.pkl', 'rb') as file:
        unpickler = CustomUnpickler(file)
        clf, tfidf_vectorizer, customTokenizer = unpickler.load()

    for index, dictionary in enumerate(data):
        #update the percentage bar as it classifies
        percentage_complete = (index + 1) / total_dicts * 100
        progress_bar['value'] = percentage_complete

        articleAbstract = dictionary["abstract"]
        articleTitle = dictionary["title"]
        dataCombined = articleAbstract + " " + articleTitle # Combining abstract and title to be analyzed
        dataCombined = [dataCombined]
        newVector = tfidf_vectorizer.transform(dataCombined)

        prediction = clf.predict(newVector)
        dictionary["ourTags"] = prediction
        np_to_fs(dictionary)

        root.update()

    return data
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC  # Import the Support Vector Machine classifier
import pandas as pd
import csv
import os
import re
import spacy
import pickle

nlp = spacy.load("en_core_web_sm") # Loading Spacy's English module

def customTokenizer(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    bigrams = [" ".join(tokens[i:i+2]) for i in range(len(tokens) - 1)]
    allGrams = tokens + bigrams
    return allGrams

def np_to_fs(og_dict):
    for k, v in og_dict.items():
        if type(v).__module__ == 'numpy':
            og_dict[k] = v.item() # Converts numpy variables to regular python variables

def add_category(progress_bar, data, root):
    progress_bar['value'] = 0
    root.update()
    total_dicts = len(data)

    with open('svm_classifier.pkl', 'rb') as file:
        clf = pickle.load(file)

    for index, dictionary in enumerate(data):
        #update the percentage bar as it classifies
        percentage_complete = (index + 1) / total_dicts * 100
        progress_bar['value'] = percentage_complete

        articleAbstract = dictionary["abstract"]
        articleTitle = dictionary["title"]
        dataCombined = articleAbstract + " " + articleTitle # Combining abstract and title to be analyzed
        dataCombined = [dataCombined]
        tfidf_vectorizer = TfidfVectorizer(tokenizer=customTokenizer, lowercase=True, token_pattern=None)
        newVector = tfidf_vectorizer.transform(dataCombined)

        prediction = clf.predict(newVector)
        dictionary["ourTags"] = prediction
        np_to_fs(dictionary)

        root.update()

    return data

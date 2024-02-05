from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC  # Import the Support Vector Machine classifier
import pandas as pd
import csv
import os
import re
import spacy

nlp = spacy.load("en_core_web_sm") # Loading Spacy's English module

def customTokenizer(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop] # Extracts lemmatized tokens
    bigrams = [" ".join(tokens[i:i+2]) for i in range(len(tokens) - 1)] # Creating bigrams to give more context to algorithm
    allGrams = tokens + bigrams # Joining bigrams and tokens

    return allGrams

def add_category(progress_bar, data):
    csvName = "allData.csv"
    allData = pd.read_csv(csvName, encoding="utf-8")  # Reading the data from allData.csv

    abstracts = allData["Abstract"].tolist()  # Extracting abstracts from the CSV
    titles = allData["Title"].tolist()  # Extracting titles from the CSV
    tags = allData["Tags"].tolist() # Extracting tags from the CSV
    labels = allData["Category"].tolist()  # Extracting labels from the CSV

    combinedFeatures = []
    for title, abstract, tag in zip(titles, abstracts, tags):
        if title and abstract and tag:
            combinedFeatures.append(f"{title} {abstract} {tag}") # Combining features of articles

    tfidf_vectorizer = TfidfVectorizer(tokenizer=customTokenizer, lowercase=True)
    vectors = tfidf_vectorizer.fit_transform(combinedFeatures) # Vectorizing and tokenizing the contents of the abstracts, titles, and tags   

    svm = SVC(C=1.0, kernel='linear', random_state=42)  # Initializing SVM
    svm.fit(vectors, labels) 

    #for the percentage bar, calculate how many dictionaries in the array
    total_dicts = len(data)

    for index, dictionary in enumerate(data):
        articleAbstract = dictionary["abstract"]
        articleTitle = dictionary["title"]
        dataCombined = articleAbstract + " " + articleTitle # Combining abstract and title to be analyzed
        dataCombined = [dataCombined]
        newVector = tfidf_vectorizer.transform(dataCombined)

        prediction = svm.predict(newVector)
        dictionary["ourTags"] = prediction

        #update the percentage bar as it classifies
        percentage_complete = (index + 1) / total_dicts * 100
        progress_bar['value'] = percentage_complete

    return data

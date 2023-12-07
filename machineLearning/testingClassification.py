from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC  # Import the Support Vector Machine classifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.preprocessing import MaxAbsScaler
import pandas as pd
import csv
import os
import re
import spacy
import json

csvName = "allData.csv"
allData = pd.read_csv(csvName, encoding="utf-8")  # Reading the data from allData.csv

jsonPath = "Articles.json"
with open(jsonPath, "r", encoding="utf-8") as jsonFile:
    testData = json.load(jsonFile)

newTitles = [item["title"] for item in testData]
newAbstracts = [item["abstract"] for item in testData]

newCombinedFeatures = [f"{title} {abstract}" for title, abstract in zip(newTitles, newAbstracts)]

nlp = spacy.load("en_core_web_sm") # Loading Spacy's English module

abstracts = allData["Abstract"].tolist()  # Extracting abstracts from the CSV
titles = allData["Title"].tolist()  # Extracting titles from the CSV
tags = allData["Tags"].tolist() # Extracting tags from the CSV
labels = allData["Category"].tolist()  # Extracting labels from the CSV

def customTokenizer(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop] # Extracts lemmatized tokens
    bigrams = [" ".join(tokens[i:i+2]) for i in range(len(tokens) - 1)] # Creating bigrams to give more context to algorithm
    allGrams = tokens + bigrams # Joining bigrams and tokens

    return allGrams

combinedFeatures = []
for title, abstract, tag in zip(titles, abstracts, tags):
    if title and abstract and tag:
        combinedFeatures.append(f"{title} {abstract} {tag}") # Combining features of articles

scaler = MaxAbsScaler()        

tfidf_vectorizer = TfidfVectorizer(tokenizer=customTokenizer, lowercase=True)
vectors = tfidf_vectorizer.fit_transform(combinedFeatures) # Vectorizing and tokenizing the contents of the abstracts, titles, and tags
vectorsScaled = scaler.fit_transform(vectors) # Normalizing data from articles
newVectors = tfidf_vectorizer.transform(newCombinedFeatures)
newVectorsScaled = scaler.fit_transform(newVectors) # Normalizing new data that is being tested

svm = SVC(C=1.0, kernel='linear', random_state=42)  # Initializing SVM
svm.fit(vectorsScaled, labels) 

newPredictions = svm.predict(newVectorsScaled) # Making predictions using the new data
for title, prediction in zip(newTitles, newPredictions):
    print(f"Title: {title}\tPrediction: {prediction}")
    print("") # Printing article titles along with predictions  
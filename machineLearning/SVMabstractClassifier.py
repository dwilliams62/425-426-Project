from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC  # Import the Support Vector Machine classifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import MaxAbsScaler
import pandas as pd
import csv
import os
import re
import spacy

csvName = "allData.csv"
allData = pd.read_csv(csvName, encoding="utf-8")  # Reading the data from allData.csv

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
        combinedFeatures.append(f"{title} {abstract} {tag}") # Combining titles, abstracts, and tags together

scaler = MaxAbsScaler()

tfidf_vectorizer = TfidfVectorizer(tokenizer=customTokenizer, lowercase=True)
vectors = tfidf_vectorizer.fit_transform(combinedFeatures) # Vectorizing and tokenizing the contents of the abstracts, titles, and tags
vectorsScaled = scaler.fit_transform(vectors) # Normalizing the vectors

svm = SVC(C=1.0, kernel='linear', random_state=42)  # Initializing SVM

X_train, X_test, y_train, y_test = train_test_split(vectorsScaled, labels, test_size=0.5, random_state=42) # Splitting training and testing data

svm.fit(X_train, y_train)  # Fitting the training data to the SVM
y_pred = svm.predict(X_test)
print(classification_report(y_test, y_pred))
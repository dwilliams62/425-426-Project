from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC  # Import the Support Vector Machine classifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
import pandas as pd
import csv
import os
import re
import spacy

csvPath = r"C:\Users\Olivia\Documents\Fall 2023\COSC 425\Training CSVs\allData.csv"
allData = pd.read_csv(csvPath, encoding="utf-8")  # Read the data from allData.csv

nlp = spacy.load("en_core_web_sm") # Loading Spacy's English module

abstracts = allData["Abstract"].tolist()  # Extract abstracts from the CSV
titles = allData["Title"].tolist()  # Extract titles from the CSV
labels = allData["Category"].tolist()  # Extract labels from the CSV

def customTokenizer(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    bigrams = [" ".join(tokens[i:i+2]) for i in range(len(tokens) - 1)] # Creating bigrams to give more context to algorithm
    all_grams = tokens + bigrams # Joining bigrams and tokens

    return all_grams

combinedFeatures = [f"{title} {abstract}" for title, abstract in zip(titles, abstracts)]

tfidf_vectorizer = TfidfVectorizer(tokenizer=customTokenizer, lowercase=True)
vectors = tfidf_vectorizer.fit_transform(combinedFeatures) # Vectorizing and tokenizing the contents of the abstracts and titles

svm = SVC(C=1.0, kernel='linear', random_state=42)  # Initializing Support Vector Machines

skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42) # Using KFold to split data into different sections

classification_reports = []

for train_indices, test_indices in skf.split(vectors, labels):
    X_train, X_test = vectors[train_indices], vectors[test_indices]
    y_train, y_test = [labels[i] for i in train_indices], [labels[i] for i in test_indices]

    svm.fit(X_train, y_train)  # Fitting the training data to the SVM
    y_pred = svm.predict(X_test)

    report = classification_report(y_test, y_pred)
    classification_reports.append(report) # Each report is appended to the report array

overall_report = classification_report(labels, svm.predict(vectors))
print("Overall Classification Report:")
print(overall_report)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import spacy
import os
import random
import pickle

# Load spaCy
nlp = spacy.load("en_core_web_sm")

# Load your CSV data
csvName = "allData.csv"
allData = pd.read_csv(csvName, encoding="utf-8")

# Define your custom tokenizer
def customTokenizer(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    bigrams = [" ".join(tokens[i:i+2]) for i in range(len(tokens) - 1)]
    allGrams = tokens + bigrams
    return allGrams

# Combine text data before vectorization
titles = allData["Title"].tolist()
abstracts = allData["Abstract"].tolist()
tags = allData["Tags"].tolist()
labels = allData["Category"].tolist()

combinedFeatures = [f"{title} {abstract} {tag}" for title, abstract, tag in zip(titles, abstracts, tags) if title and abstract]

# Vectorize using TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(tokenizer=customTokenizer, lowercase=True, token_pattern=None)
vectors = tfidf_vectorizer.fit_transform(combinedFeatures)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(vectors, labels, test_size=0.4, random_state=42)

# Train SVM classifier
clf = SVC(C=1, gamma="scale", kernel="linear")
clf.fit(X_train, y_train)

with open('svm_classifier.pkl', 'wb') as file:
    pickle.dump((clf, tfidf_vectorizer, customTokenizer), file)
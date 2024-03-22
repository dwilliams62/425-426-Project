from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import spacy
import os
import random
import pickle

#Loading spacy's English module
nlp = spacy.load("en_core_web_sm")

#Loading data from the CSV containing Dr. Maier's dataset
csvName = "allData.csv"
allData = pd.read_csv(csvName, encoding="utf-8")

#Custom tokenizer to be used by vectorizer
def customTokenizer(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    bigrams = [" ".join(tokens[i:i+2]) for i in range(len(tokens) - 1)] #Using bigrams gives more context
    allGrams = tokens + bigrams
    return allGrams

#Combining all text data together before vectorization
titles = allData["Title"].tolist()
abstracts = allData["Abstract"].tolist()
tags = allData["Tags"].tolist()
labels = allData["Category"].tolist()

combinedFeatures = [f"{title} {abstract} {tag}" for title, abstract, tag in zip(titles, abstracts, tags) if title and abstract]

#Vectorizing using tfidf vectorizer and the custom tokenizer created earlier
tfidf_vectorizer = TfidfVectorizer(tokenizer=customTokenizer, lowercase=True, token_pattern=None)
vectors = tfidf_vectorizer.fit_transform(combinedFeatures)

#Splitting the data into testing and training sets
X_train, X_test, y_train, y_test = train_test_split(vectors, labels, test_size=0.4, random_state=42)

#Training the SVM classifier
clf = SVC(C=1, gamma="scale", kernel="linear")
clf.fit(X_train, y_train)

#After training the classifier, pickle everything so it can be used for the executable
with open('svm_classifier.pkl', 'wb') as file:
    pickle.dump((clf, tfidf_vectorizer, customTokenizer), file)
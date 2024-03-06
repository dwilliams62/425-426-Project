from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import spacy
import os

csvName = "allData.csv"
allData = pd.read_csv(csvName, encoding="utf-8")

os.environ["OMP_NUM_THREADS"] = "2"

nlp = spacy.load("en_core_web_sm")

abstracts = allData["Abstract"].tolist()
titles = allData["Title"].tolist()
tags = allData["Tags"].tolist()
labels = allData["Category"].tolist()

def customTokenizer(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    bigrams = [" ".join(tokens[i:i+2]) for i in range(len(tokens) - 1)] 
    allGrams = tokens + bigrams
    return " ".join(allGrams)

# Combine text data before vectorization
combinedFeatures = [customTokenizer(f"{title} {abstract} {tag}") for title, abstract, tag in zip(titles, abstracts, tags) if title and abstract]

# Use TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(lowercase=True)
vectors = tfidf_vectorizer.fit_transform(combinedFeatures)

# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(vectors, labels, test_size=0.4, random_state=42)

# Creating SVM classifier
clf = SVC(C=1, gamma="scale", kernel="linear")
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
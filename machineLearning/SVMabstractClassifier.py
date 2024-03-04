from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from gensim.models import Word2Vec
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
    return allGrams

# Combine text data before vectorization
combinedFeatures = [customTokenizer(f"{title} {abstract} {tag}") for title, abstract, tag in zip(titles, abstracts, tags) if title and abstract]
combinedFeatures = [feature if pd.notna(feature) else "" for feature in combinedFeatures]

# Train Word2Vec model
word2vec_model = Word2Vec(sentences=combinedFeatures, vector_size=100, window=5, min_count=1, workers=2)

# Transform each document into a concatenated vector
document_vectors = []
for doc_tokens in combinedFeatures:
    vectors = [word2vec_model.wv[token] for token in doc_tokens if token in word2vec_model.wv]
    if vectors:
        document_vector = [item for sublist in vectors for item in sublist]
        document_vectors.append(document_vector)
    else:
        # If no vectors are available, use zeros
        document_vectors.append([0] * (len(doc_tokens) * 100))

# Convert to dense array
vectors = pd.DataFrame(document_vectors).to_numpy()

# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(vectors, labels, test_size=0.4, random_state=42)

# Creating SVM classifier
clf = SVC(C=1, gamma="scale", kernel="linear")
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
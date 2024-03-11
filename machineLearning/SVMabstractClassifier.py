import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import spacy
import os
import random

# Download NLTK data
nltk.download('wordnet')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

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

# Function for synonym replacement
def synonym_replacement(words, n=1):
    new_words = words.copy()
    random_word_list = list(set([word for word in words if word not in stop_words]))
    random.shuffle(random_word_list)
    num_replaced = 0

    for random_word in random_word_list:
        synonyms = get_synonyms(random_word)
        if len(synonyms) > 0:
            synonym = random.choice(synonyms)
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1

        if num_replaced >= n:
            break

    return new_words

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace("_", " ").replace("-", " ").lower()
            synonyms.add(synonym)
    return list(synonyms)

# Apply synonym replacement to combined features
augmented_combinedFeatures = []
for feature in combinedFeatures:
    words = feature.split()
    augmented_words = synonym_replacement(words)
    augmented_feature = " ".join(augmented_words)
    augmented_combinedFeatures.append(augmented_feature)

# Vectorize using TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(tokenizer=customTokenizer, lowercase=True, token_pattern=None)
vectors = tfidf_vectorizer.fit_transform(augmented_combinedFeatures)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(vectors, labels, test_size=0.4, random_state=42)

# Train SVM classifier
clf = SVC(C=1, gamma="scale", kernel="linear")
clf.fit(X_train, y_train)

# Predict and evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
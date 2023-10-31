from sklearn.feature_extraction.text import TfidfVectorizer # For vectorization of text data
from sklearn.naive_bayes import MultinomialNB # Naive Bayes algorithm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_predict
import csv
import os
import re
import spacy

csvPath = r"C:\Users\Olivia\Documents\Fall 2023\COSC 425\Training CSVs" # Path to CSV files
abstracts = [] # Array for holding the abstracts
labels = [] # Array for holding the labels each abstract falls under

nlp = spacy.load("en_core_web_sm") # Loading spacy's English module

def customTokenizer(text):
    doc = nlp(text) # Using spacy to process the abstracts
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop] # Getting the tokens
    bigrams = [" ".join(tokens[i:i+2]) for i in range(len(tokens) - 1)] # Using bigrams to give the algorithm more context
    all_grams = tokens + bigrams
    words = [word.lower() for word in all_grams if re.match("^[a-zA-Z]+$", word)] # Making sure the tokens are alphabetical

    return tokens

for filename in os.listdir(csvPath):
    if filename.endswith(".csv"):
        category = os.path.splitext(filename)[0] # Extracts the category label from the file name

        with open(os.path.join(csvPath, filename), mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                abstract = row["Abstract Note"]
                if abstract.strip(): # Doesn't extract abstract if there is a blank space
                    abstracts.append(row["Abstract Note"]) # Extracts abstracts from the abstract column in the CSV
                    labels.append(category)
        
tfidf_vectorizer = TfidfVectorizer(tokenizer=customTokenizer, lowercase=True, stop_words='english')      
vectors = tfidf_vectorizer.fit_transform(abstracts) # Vectorizing the abstracts

nb = MultinomialNB() # Loading in multinomial Naive Bayes

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42) # Cross validation for the testing data

classification_reports = [] # Array to store multiple classification reports 

for train_indices, test_indices in skf.split(vectors, labels):
    X_train, X_test = vectors[train_indices], vectors[test_indices]
    y_train, y_test = [labels[i] for i in train_indices], [labels[i] for i in test_indices]

    nb.fit(X_train, y_train) # Fitting training and testing data to the algorithm
    y_pred = nb.predict(X_test)

    report = classification_report(y_test, y_pred)
    classification_reports.append(report) # Appends a machine learning algorithm for each fold

overall_report = classification_report(labels, nb.predict(vectors)) # Classification report for all of the data
print("Overall Classification Report:")
print(overall_report)       

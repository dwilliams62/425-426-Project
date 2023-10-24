from sklearn.feature_extraction.text import TfidfVectorizer # For vectorization of text data
from sklearn.naive_bayes import MultinomialNB # Naive Bayes algorithm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import csv
import os
import nltk # For tokenization of data
from nltk.tokenize import word_tokenize

csvPath = r"C:\Users\Olivia\Documents\Fall 2023\COSC 425\Training CSVs" # Path to CSV files
abstracts = [] # Array for holding the abstracts
labels = [] # Array for holding the labels each abstract falls under

def customTokenizer(text):
    words = word_tokenize(text)
    return words

tfidf_vectorizer = TfidfVectorizer(tokenizer=customTokenizer, lowercase=True, stop_words='english')

for filename in os.listdir(csvPath):
    if filename.endswith(".csv"):
        category = os.path.splitext(filename)[0] # Extracts the category label from the file name

        with open(os.path.join(csvPath, filename), mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                abstracts.append(row["Abstract Note"]) # Extracts abstracts from the abstract column in the CSV
                labels.append(category)
        
vectors = tfidf_vectorizer.fit_transform(abstracts) # Vectorizing the abstracts

X_train, X_test, y_train, y_test = train_test_split(
    vectors,  
    labels,           
    test_size=0.1, # What percentage of data will be used for testing
    random_state=42 # Seed for splitting the data up  
)   

nb = MultinomialNB()
nb.fit(X_train, y_train)
y_pred = nb.predict(X_test) # Using the training data to make predictions

report = classification_report(y_pred, y_test)
print(report) # This report displays the accuracy for predictions made by our algorithm with the current data      

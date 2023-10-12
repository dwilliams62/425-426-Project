import os
from sklearn.feature_extraction.text import TfidfVectorizer
# Importing naive bayes algorithm from SciKit
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def load_and_preprocess_text_files(directory_path):
    text_samples = [] # Stores the content of the .txt files
    labels = [] # Stores the category names found in the .txt files
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path, filename), "r", encoding="utf-8") as file:
                # Storing the meaningful content of the file
                content = file.read()
                # When this symbol is encountered, the file splits off and the category is after the |
                parts = content.split("|")
                if(len(parts) == 2):
                    text = parts[0].strip()
                    category = parts[1].strip()
                    text_samples.append(text)
                    labels.append(category)
    return text_samples, labels

text_directory = r"C:\Users\Olivia\Documents\Fall 2023\COSC 425\Test Code"
text_samples, labels = load_and_preprocess_text_files(text_directory)

tfidf_vectorizer = TfidfVectorizer() 
tfidf_vectors = tfidf_vectorizer.fit_transform(text_samples) # Vectorizing the text samples so they can be understood and processed by the Naive Bayes algorithm

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    tfidf_vectors,  
    labels,           
    test_size=0.1,
    random_state=42 # Seed for splitting the data up  
)

nb = MultinomialNB()
nb.fit(X_train, y_train)
y_pred = nb.predict(X_test) # Using the training data to make predictions

report = classification_report(y_pred, y_test)
print(report) # This report displays the accuracy for predictions made by our algorithm with the current data
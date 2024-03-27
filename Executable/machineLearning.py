from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import spacy
import os
import random
import pickle

#Loads spacy's English module
nlp = spacy.load("en_core_web_sm")

#Custom tokenizer to be used by vectorizer
def customTokenizer(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    bigrams = [" ".join(tokens[i:i+2]) for i in range(len(tokens) - 1)] #Using bigrams gives more context
    allGrams = tokens + bigrams
    return allGrams

#Fixes issues related to numpy objects with the machine learning
def np_to_fs(og_dict):
    for k, v in og_dict.items():
        if type(v).__module__ == 'numpy':
            og_dict[k] = v.item() #Converts numpy variables to regular python variables

def add_category(progress_bar, data, root):
    csvName = "allData.csv"
    allData = pd.read_csv(csvName, encoding="utf-8")  # Reading the data from allData.csv
    progress_bar['value'] = 30
    root.update()

    #Combining all text data together before vectorization
    titles = allData["Title"].tolist()
    abstracts = allData["Abstract"].tolist()
    tags = allData["Tags"].tolist()
    labels = allData["Category"].tolist()

    combinedFeatures = [f"{title} {abstract} {tag}" for title, abstract, tag in zip(titles, abstracts, tags) if title and abstract]
    progress_bar['value'] = 60
    root.update()        

    tfidf_vectorizer = TfidfVectorizer(tokenizer=customTokenizer, lowercase=True)
    vectors = tfidf_vectorizer.fit_transform(combinedFeatures) # Vectorizing and tokenizing the contents of the abstracts, titles, and tags   
    progress_bar['value'] = 90 # Vectorization is slow and will probably hang here for a minute
    root.update()  

    svm = SVC(C=1.0, kernel='linear', gamma="scale", random_state=42)  # Initializing SVM
    svm.fit(vectors, labels) 
    progress_bar['value'] = 100
    root.update()

    #for the percentage bar, calculate how many dictionaries in the array
    total_dicts = len(data)

    progress_bar['value'] = 0
    root.update()

    for index, dictionary in enumerate(data):
        #update the percentage bar as it classifies
        percentage_complete = (index + 1) / total_dicts * 100
        progress_bar['value'] = percentage_complete

        articleAbstract = dictionary["abstract"]
        articleTitle = dictionary["title"]
        dataCombined = f"{articleTitle} {articleAbstract}"  # Combine abstract, title, and tag

        newVectors = tfidf_vectorizer.transform([dataCombined]) # Vectorizing and tokenizing the contents of the abstracts, titles, and tags   

        prediction = svm.predict(newVectors)

        dictionary["ourTags"] = prediction
        np_to_fs(dictionary)

        #update the percentage bar as it classifies
        percentage_complete = (index + 1) / total_dicts * 100
        progress_bar['value'] = percentage_complete
        root.update()

    return data
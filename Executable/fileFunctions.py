import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

from rdflib import Graph


cred = credentials.Certificate("FirebaseInfo.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def process_file(file_path):
    with open(file_path, 'r') as file:
        processed_data = json.load(file)

    for dictionary in processed_data:
        authors = dictionary['author']
        for i, author_info in enumerate(authors, start=1):
            key = f'author{i}'
            author_string = f"{author_info['given']} {author_info['family']}"
            dictionary[key] = author_string
        del dictionary['author']

    return processed_data

def upload_to_website(data):
    #connect to cloud firestore database. atm requires a FirebaseInfo.json that for security purposes will not be uploaded to the github


    #for every article passed to it, creates a new document in the Documents collection with the document ID as the title
    for article in data:
        document_id = article['title'].replace(" ", "")
        doc_ref = db.collection("Documents").document(document_id)
        doc_ref.set(article)

def download_data(data, file_path, file_name):
    csl_json = json.dumps(data, indent=4)

    full_file_path = f"{file_path}/{file_name}.json"

    with open(full_file_path, 'w') as file:
        file.write(csl_json)

    print(f"File '{file_name}' has been created.")


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def process_rdf_file(file_path):
    # Add your processing logic here to handle the RDF file
    # Perform operations and return the processed data
    processed_data = f"Processed data from {file_path}"  # Placeholder example
    return processed_data

def upload_to_website(data):
    #connect to cloud firestore database. atm requires a FirebaseInfo.json that for security purposes will not be uploaded to the github
    cred = credentials.Certificate("FirebaseInfo.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    #for every article passed to it, creates a new document in the Documents collection with the document ID as the title
    for article in data:
        document_id = article['title']
        doc_ref = db.collection("Documents").document(document_id)
        doc_ref.set({"Title": article['title'], "URL": article['url'], "PubTitle": article['pubTitle'], "PubYear": article['pubYear'], 
            "Authors": article['author'], "Date":article['date'], "DOI":article['doi'], "Volume":article['volume'], "ISSN":article['issn'],
            "Abstract":article['abstract'], "Item Type":article['itemType'], "LibCatalog":article['libCatalog'], 
            "Classification":article['ourTags']})

def download_as_rdf(data):
    print("download")


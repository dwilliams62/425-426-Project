import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from rdflib import Graph

def process_rdf_file(file_path):
    # Add your processing logic here to handle the RDF file
    # Perform operations and return the processed data

    g = Graph()
    g.parse(file_path, format='xml')
    
    # SPARQL query to find all unique ISSNs and associated data
    sparql_query = """
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        SELECT ?s ?p ?o
        WHERE {
            ?s dc:identifier ?issn .
            ?s ?p ?o .
            FILTER regex(str(?issn), "^[0-9]{4}-[0-9]{4}$")
        }
    """
    
    # Execute the SPARQL query
    query_results = g.query(sparql_query)
    
    # Store information for each ISSN
    issn_data = {}
    
    # Collect information for each ISSN
    for result in query_results:
        issn = result['issn']
        subj = result['s']
        pred = result['p']
        obj = result['o']
        
        if issn not in issn_data:
            issn_data[issn] = []
        
        issn_data[issn].append({'subject': subj, 'predicate': pred, 'object': obj})
    
    # Print information grouped by ISSN
    for issn, data in issn_data.items():
        print(f"ISSN: {issn}")
        for item in data:
            print(f"  Subject: {item['subject']}")
            print(f"  Predicate: {item['predicate']}")
            print(f"  Object: {item['object']}")
        print()
    
    processed_data = f"Processed data from {file_path}"  # Placeholder example
    return processed_data

def upload_to_website(data):
    #connect to cloud firestore database. atm requires a FirebaseInfo.json that for security purposes will not be uploaded to the github
    cred = credentials.Certificate("FirebaseInfo.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    #for every article passed to it, creates a new document in the Documents collection with the document ID as the title
    for article in data:
        document_id = article['title'].replace(" ", "")
        doc_ref = db.collection("Documents").document(document_id)
        doc_ref.set({"Title": article['title'], "URL": article['url'], "PubTitle": article['pubTitle'], "PubYear": article['pubYear'], 
            "Authors": article['author'], "Date":article['date'], "DOI":article['doi'], "Volume":article['volume'], "ISSN":article['issn'],
            "Abstract":article['abstract'], "Item Type":article['itemType'], "LibCatalog":article['libCatalog'], 
            "Classification":article['ourTags'],"Affiliations":article['affiliation']})

def download_as_rdf(data):
    print("download")


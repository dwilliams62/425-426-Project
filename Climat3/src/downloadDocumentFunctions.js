//Import the functions you need from firebase firestore
import { initializeApp } from "firebase/app";
import { getFirestore, doc, getDoc } from "firebase/firestore";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAiI2TJwXB8Zyg9GWKspaqpVlFPtFpShu8",
  authDomain: "climat3.firebaseapp.com",
  databaseURL: "https://climat3-default-rtdb.firebaseio.com",
  projectId: "climat3",
  storageBucket: "climat3.appspot.com",
  messagingSenderId: "80202285914",
  appId: "1:80202285914:web:b3f8446bbd1a88dafea963",
  measurementId: "G-XXWF74D2S0"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Initialize the currently selected articles array
var selectedArticles = [];

function addArticleToArray(item) {
  if (!selectedArticles.includes(item)) {
    selectedArticles.push(item);
  }
}

function removeArticleFromArray(item) {
  if (selectedArticles.includes(item)) {
    selectedArticles = selectedArticles.filter(selected => selected !== item);
  }
}

export function UpdateSelectedArray(event) {
  var ArticleTitle = this.parentNode.textContent.trim();

  if (event.target.checked) {
    addArticleToArray(ArticleTitle); // Add the Article if checkbox is checked
  } else {
    removeArticleFromArray(ArticleTitle); // Remove the item if checkbox is unchecked
  }

  console.log(selectedArticles); // Display the updated array
}

//turns the string into a blob that is then downloaded as a .rdf file
export async function DownloadXMLRDF() {
  var RDFFile = await(CreateSelectedArticlesRDF());

  var link = document.createElement('a');
  link.download = 'data.rdf';
  var blob = new Blob([RDFFile], {type: 'text/plain'});
  link.href = window.URL.createObjectURL(blob);
  link.click();
}

async function CreateSelectedArticlesRDF() {
  var articleRDFString = addHeadingRDFFile();

  for (let i = 0; i < selectedArticles.length; i++) {
    var tempStr = selectedArticles[i].replace(/\s/g, "");
    var docRef = doc(db, 'Documents', tempStr);
    var docSnap = await getDoc(docRef);
    if (docSnap.exists()) {
      console.log("Document data:", docSnap.data());
      articleRDFString += addArticleRDFFile(docSnap);
    } else {
      console.log("No such document named " + selectedArticles[i] + " in the collection Documents.");
    }
  }

  //end the rdf file
  articleRDFString += '</rdf:RDF>';
  console.log(articleRDFString);
  return articleRDFString;
}

//this is just the header of an RDF file that we add first
function addHeadingRDFFile() {
  var articleRDFString = "<rdf:RDF\n";
  articleRDFString += 'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
  articleRDFString += 'xmlns:z="http://www.zotero.org/namespaces/export#"\n'
  articleRDFString += 'xmlns:dcterms="http://purl.org/dc/terms/"\n'
  articleRDFString += 'xmlns:bib="http://purl.org/net/biblio#"\n'
  articleRDFString += 'xmlns:foaf="http://xmlns.com/foaf/0.1/"\n'
  articleRDFString += 'xmlns:dc="http://purl.org/dc/elements/1.1/"\n'
  articleRDFString += 'xmlns:prism="http://prismstandard.org/namespaces/1.2/basic/">\n'
  return articleRDFString;
}

//for each article we go through and add this one by one. there will be more functions in here for each piece. 
//takes a reference to a document gathered from the database as a parameter
function addArticleRDFFile(document) {
    var articleRDFString = '<bib:Article rdf:about="' + document.data().URL + '">\n';
    articleRDFString += '<z:itemType>journalArticle</z:itemType>\n';
    articleRDFString += '<dcterms:isPartOf rdf:resource="urn:issn:' + document.data().ISSN + '"/>\n';
    articleRDFString += '<bib:authors>\n';
    articleRDFString += '<rdf:Seq>\n';
    articleRDFString += '<rdf:li>\n';
    articleRDFString += '<foaf:Person>\n';
    articleRDFString += '<foaf:surname>' + document.data().Authors + '</foaf:surname>\n';
    articleRDFString += '<foaf:givenName>' + 'Author First Name' + '</foaf:givenName>\n';
    articleRDFString += '</foaf:Person>\n';
    articleRDFString += '</rdf:li>\n';
    articleRDFString += '</rdf:Seq>\n';
    articleRDFString += '</bib:authors>\n';
    articleRDFString += '<dc:subject>' + 'document.data().manualTags' + '</dc:subject>\n';
    articleRDFString += '<dc:title>' + document.data().Title + '</dc:title>\n';
    articleRDFString += '<dcterms:abstract>' + document.data().Abstract + '</dcterms:abstract>\n';
    articleRDFString += '<dc:date>' + document.data().Date + '</dc:date>\n';
    articleRDFString += '<z:language>' + 'English' + '</z:language>\n';
    articleRDFString += '<dc:identifier>\n';
    articleRDFString += '<dcterms:URI><rdf:value>' + document.data().URL + '</rdf:value></dcterms:URI>\n';
    articleRDFString += '</dc:identifier>\n';
    articleRDFString += '<dcterms:dateSubmitted>' + '2023-11-18' + '</dcterms:dateSubmitted>\n';
    articleRDFString += '</bib:Article>\n'
    articleRDFString += '<bib:Journal rdf:about="urn:issn:' + document.data().ISSN + '">\n';
    articleRDFString += '<prism:volume>' + document.data().Volume + '</prism:volume>\n';
    articleRDFString += '<dc:title>' + document.data().PubTitle + '</dc:title>\n';
    articleRDFString += '<dc:identifier>' + document.data().DOI + '</dc:identifier>\n';
    articleRDFString += '<prism:number>' + document.data().Issue + '</prism:number>\n';
    articleRDFString += '<dc:identifier>' + document.data().ISSN + '</dc:identifier>\n';
    articleRDFString += '</bib:Journal>\n';
    return articleRDFString;
}
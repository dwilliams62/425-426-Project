//Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore, doc, setDoc, getDoc } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

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

console.log('Hello Firebase!');

function addNewDocument() {
  setDoc(doc(db, document.getElementById('collecName').value, document.getElementById('docName').value), {
    customer: document.getElementById('custName').value,
    testString: 'updated'
  });
  console.log("Added!");
}

async function printFile() {
  var reader = new FileReader();
  // reader.addEventListener('load', function() {
  //   document.getElementById('file').innerText = this.result;
  // });
  reader.readAsText(document.querySelector('.input').files[0]);
  reader.onload = onReaderLoad;
}

function onReaderLoad(event){
    console.log(event.target.result);
    var obj = JSON.parse(event.target.result);
    var len = Object.keys(obj).length;
    var str = "DocName";
    var count = str.match(/\d*$/);

    for (let i = 0; i < len; i++) {
      setDoc(doc(db, document.getElementById('collecName').value, str.substr(0, count.index) + (++count[0])), {
        itemType: obj[i]['itemType'],
        title: obj[i]['title'],
        pubTitle: obj[i]['pubTitle'],
        author: obj[i]['author'],
        pubYear: obj[i]['pubYear'],
        doi: obj[i]['doi'],
        url: obj[i]['url'],
        abstract: obj[i]['abstract'],
        date: obj[i]['date'],
        volume: obj[i]['volume'],
        issue: obj[i]['issue'],
        issn: obj[i]['issn'],
        libCatalog: obj[i]['libCatalog'],
        manualTags: obj[i]['manualTags'],
        autoTags: obj[i]['autoTags']
      });
      console.log("Added!");
    }
}

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

function addArticleRDFFile(document) {
  var articleRDFString = '<bib:Article rdf:about="' + document.data().url + '">\n';
  articleRDFString += '<z:itemType>journalArticle</z:itemType>\n';
  articleRDFString += '<dcterms:isPartOf rdf:resource="urn:issn:' + document.data().issn + '"/>\n';
  articleRDFString += '<bib:authors>\n';
  articleRDFString += '<rdf:Seq>\n';
  articleRDFString += '<rdf:li>\n';
  articleRDFString += '<foaf:Person>\n';
  articleRDFString += '<foaf:surname>' + document.data().author + '</foaf:surname>\n';
  articleRDFString += '<foaf:givenName>' + 'Author First Name' + '</foaf:givenName>\n';
  articleRDFString += '</foaf:Person>\n';
  articleRDFString += '</rdf:li>\n';
  articleRDFString += '</rdf:Seq>\n';
  articleRDFString += '</bib:authors>\n';
  articleRDFString += '<dc:subject>' + 'document.data().manualTags' + '</dc:subject>\n';
  articleRDFString += '<dc:title>' + document.data().title + '</dc:title>\n';
  articleRDFString += '<dcterms:abstract>' + document.data().abstract + '</dcterms:abstract>\n';
  articleRDFString += '<dc:date>' + document.data().date + '</dc:date>\n';
  articleRDFString += '<z:language>' + 'English' + '</z:language>\n';
  articleRDFString += '<dc:identifier>\n';
  articleRDFString += '<dcterms:URI><rdf:value>' + document.data().url + '</rdf:value></dcterms:URI>\n';
  articleRDFString += '</dc:identifier>\n';
  articleRDFString += '<dcterms:dateSubmitted>' + '2023-11-18' + '</dcterms:dateSubmitted>\n';
  articleRDFString += '</bib:Article>\n'
  articleRDFString += '<bib:Journal rdf:about="urn:issn:' + document.data().issn + '">\n';
  articleRDFString += '<prism:volume>' + document.data().volume + '</prism:volume>\n';
  articleRDFString += '<dc:title>' + document.data().pubTitle + '</dc:title>\n';
  articleRDFString += '<dc:identifier>' + document.data().doi + '</dc:identifier>\n';
  articleRDFString += '<prism:number>' + document.data().issue + '</prism:number>\n';
  articleRDFString += '<dc:identifier>' + document.data().issn + '</dc:identifier>\n';
  articleRDFString += '</bib:Journal>\n';
  return articleRDFString;
}

async function CreateXMLRDFFile(collectionName, documentName) {
  var articleRDFString = addHeadingRDFFile();

  var str = "DocName";
  var count = str.match(/\d*$/);

  for (var i = 0; i < 2; i++) {
    var docRef = doc(db, collectionName, str.substr(0, count.index) + (++count[0]));
    var docSnap = await getDoc(docRef);
    if (docSnap.exists()) {
      console.log("Document data:", docSnap.data());
    } else {
      console.log("No such document named " + documentName + " in the collection "+ collectionName + ".");
    }
    articleRDFString += addArticleRDFFile(docSnap);
  }

  articleRDFString += '</rdf:RDF>';

  console.log(articleRDFString);
  return articleRDFString;
}

async function CreateXMLRDF() {
  var RDFFile = await(CreateXMLRDFFile('delete', 'DocName1'));

  var link = document.createElement('a');
  link.download = 'data.rdf';
  var blob = new Blob([RDFFile], {type: 'text/plain'});
  link.href = window.URL.createObjectURL(blob);
  link.click();
}

document.getElementById('uploadBtn').addEventListener('click', printFile);
document.getElementById("myBtn").addEventListener("click", addNewDocument);
document.getElementById("openDocTest").addEventListener("click", CreateXMLRDF);


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

async function CreateXMLRDF() {
  const docRef = doc(db, document.getElementById('collecName').value, document.getElementById('docName').value);
  const docSnap = await getDoc(docRef);

  if (docSnap.exists()) {
    console.log("Document data:", docSnap.data());
  } else {
    // docSnap.data() will be undefined in this case
    console.log("No such document!");
  }

  var XMLRDF = "<rdf:RDF\n";
  XMLRDF += 'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
  XMLRDF += 'xmlns:z="http://www.zotero.org/namespaces/export#"\n'
  XMLRDF += 'xmlns:dcterms="http://purl.org/dc/terms/"\n'
  XMLRDF += 'xmlns:bib="http://purl.org/net/biblio#"\n'
  XMLRDF += 'xmlns:foaf="http://xmlns.com/foaf/0.1/"\n'
  XMLRDF += 'xmlns:dc="http://purl.org/dc/elements/1.1/"\n'
  XMLRDF += 'xmlns:prism="http://prismstandard.org/namespaces/1.2/basic/">\n'
  //XMLRDF += docSnap.data().url;
  XMLRDF += '<bib:Article rdf:about="' + docSnap.data().url + '">\n';
  XMLRDF += '<z:itemType>journalArticle</z:itemType>\n';
  XMLRDF += '<dcterms:isPartOf rdf:resource="urn:issn:' + docSnap.data().issn + '"/>\n';
  XMLRDF += '<bib:authors>\n';
  XMLRDF += '<rdf:Seq>\n';
  XMLRDF += '<rdf:li>\n';
  XMLRDF += '<foaf:Person>\n';
  XMLRDF += '<foaf:surname>' + docSnap.data().author + '</foaf:surname>\n';
  XMLRDF += '<foaf:givenName>' + 'Author First Name' + '</foaf:givenName>\n';
  XMLRDF += '</foaf:Person>\n';
  XMLRDF += '</rdf:li>\n';
  XMLRDF += '</rdf:Seq>\n';
  XMLRDF += '</bib:authors>\n';
  XMLRDF += '<dc:subject>' + docSnap.data().manualTags + '</dc:subject>\n';
  XMLRDF += '<dc:title>' + docSnap.data().title + '</dc:title>\n';
  XMLRDF += '<dcterms:abstract>' + docSnap.data().abstract + '</dcterms:abstract>\n';
  XMLRDF += '<dc:date>' + docSnap.data().date + '</dc:date>\n';
  XMLRDF += '<z:language>' + 'English' + '</z:language>\n';
  XMLRDF += '<dc:identifier>\n';
  XMLRDF += '<dcterms:URI><rdf:value>' + docSnap.data().url + '</rdf:value></dcterms:URI>\n';
  XMLRDF += '</dc:identifier>\n';
  XMLRDF += '<dcterms:dateSubmitted>' + '2023-11-18' + '</dcterms:dateSubmitted>\n';
  XMLRDF += '</bib:Article>\n'
  XMLRDF += '<bib:Journal rdf:about="' + docSnap.data().issn + '">\n';
  XMLRDF += '<prism:volume>' + docSnap.data().volume + '</prism:volume>\n';
  XMLRDF += '<dc:title>' + docSnap.data().pubTitle + '</dc:title>\n';
  XMLRDF += '<dc:identifier>' + docSnap.data().doi + '</dc:identifier>\n';
  XMLRDF += '<prism:number>' + docSnap.data().issue + '</prism:number>\n';
  XMLRDF += '<dc:identifier>' + docSnap.data().issn + '</dc:identifier>\n';
  XMLRDF += '</bib:Journal>\n';
  XMLRDF += '</rdf:RDF>';

  console.log(XMLRDF);

  var link = document.createElement('a');
link.download = 'data.rdf';
var blob = new Blob([XMLRDF], {type: 'text/plain'});
link.href = window.URL.createObjectURL(blob);
link.click();
}

document.getElementById('uploadBtn').addEventListener('click', printFile);
document.getElementById("myBtn").addEventListener("click", addNewDocument);
document.getElementById("openDocTest").addEventListener("click", CreateXMLRDF);


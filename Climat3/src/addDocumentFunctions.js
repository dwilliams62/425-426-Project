//Import the functions you need from firebase firestore
import { initializeApp } from "firebase/app";
import { getFirestore, doc, setDoc } from "firebase/firestore";

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

export function addNewDocument() {
    //this will insert a document into the database
    //the first value is the database it inserts into, the second is the collection name (will create a new collection if the one of the specified
    //name does not exist), and the third is the name of the document. the fourth is then all of the data you will insert, seperated by : as follows
    setDoc(doc(db, document.getElementById('collecName').value, document.getElementById('docName').value), {
      customer: document.getElementById('custName').value,
      testString: 'updated'
    });
    console.log("Added!");
}

//this function opens the uploaded file given through the website and sends it to onReaderLoad function
export async function loadJSONDocument() {
    var reader = new FileReader();
    reader.readAsText(document.querySelector('.input').files[0]);
    reader.onload = addJSONDocument;
  }

//once the file is fully read, this function is called to parse the given JSON and then upload the information to the database using setDoc
function addJSONDocument(event){
    console.log(event.target.result); //for testing
    var obj = JSON.parse(event.target.result); //parse the data
    var len = Object.keys(obj).length; //get how many articles are in the json

    //these two are just for giving unique names to each document by incrememnting the number
    var str = "DocName";
    var count = str.match(/\d*$/);

    //loop through all the articles in the parsed json and input each into the database
    for (let i = 0; i < len; i++) {
      //sets the doc based off the provided collection name on the website and a incrememnting document name
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
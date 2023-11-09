//Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore, doc, collection, addDoc, setDoc } from "firebase/firestore";
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
  //const testCollection = collection(db, document.getElementById('collecName').value);
  //const newDoc = addDoc(testCollection, {
    //customer: document.getElementById('custName').value,
    //testString: 'updated'
  //});
  setDoc(doc(db, document.getElementById('collecName').value, document.getElementById('docName').value), {
    customer: document.getElementById('custName').value,
    testString: 'updated'
  });
  console.log("Added!");
}


async function parseJsonFile(file) {
  return new Promise((resolve, reject) => {
    const fileReader = new FileReader()
    fileReader.onload = event => resolve(JSON.parse(event.target.result))
    fileReader.onerror = error => reject(error)
    fileReader.readAsText(file)
  })
}

async function printFile() {
  var reader = new FileReader();
  reader.addEventListener('load', function() {
    document.getElementById('file').innerText = this.result;
  });
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
  
function alert_data(name, family){
    alert('Name : ' + name + ', Family : ' + family);
}

document.getElementById('uploadBtn').addEventListener('click', printFile);
document.getElementById("myBtn").addEventListener("click", addNewDocument);


//Import the functions you need from firebase firestore
import { initializeApp } from "firebase/app";
import { getFirestore, doc, setDoc } from "firebase/firestore";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyA9Qs3BoYl4Q2rbmZkXCqvlhsIWoZHZK4E",
    authDomain: "tiei-5b0c1.firebaseapp.com",
    databaseURL: "https://tiei-5b0c1-default-rtdb.firebaseio.com",
    projectId: "tiei-5b0c1",
    storageBucket: "tiei-5b0c1.appspot.com",
    messagingSenderId: "491562625266",
    appId: "1:491562625266:web:d813e4de8c6eac0a4a486b",
    measurementId: "G-EQDY7FVRN2"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export function addNewDocument() {
  console.log("Clicked!");
  console.log(document.getElementById('docName').value);
  console.log(document.getElementById('bio').value);
  console.log(document.getElementById('email').value);
  console.log(document.getElementById('first').value);
  console.log(document.getElementById('last').value);
    //this will insert a document into the database
    //the first value is the database it inserts into, the second is the collection name (will create a new collection if the one of the specified
    //name does not exist), and the third is the name of the document. the fourth is then all of the data you will insert, seperated by : as follows
    setDoc(doc(db, 'Authors', document.getElementById('docName').value), {
      Bio: document.getElementById('bio').value,
      Email: document.getElementById('email').value,
      First: document.getElementById('first').value,
      Last: document.getElementById('last').value,
      testString: 'updated'
    });
    console.log("Added!");
}

export function show() {
  console.log("Show function clicked");
  // Reference to the collection you want to display
  const collectionRef = db.collection('Authors');
  
  // Get all documents from the collection
  collectionRef.get().then((querySnapshot) => {
    const dataList = document.getElementById('dataList');
  
    // Loop through each document
    querySnapshot.forEach((doc) => {
      // Access the document data
      const data = doc.data();
  
      // Create a list item for each document
      const listItem = document.createElement('li');
      listItem.textContent = JSON.stringify(data);
  
      // Append the list item to the unordered list
      dataList.appendChild(listItem);
    });
  }).catch((error) => {
    console.error("Error getting documents: ", error);
  });
  }
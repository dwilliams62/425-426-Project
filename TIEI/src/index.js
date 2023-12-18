import { addNewDocument, show } from "./addDocumentFunctions.js";
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

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

console.log('Hello Firebase!'); //just to show it's working in console (fn f12 i think?)

//add listeners to the buttons needed


//this button is a simple test button to see how things work. it will get the collection name, document name, and the value of
//customer that the user defines in databasetest.html, and upload a document with that information into the database
document.getElementById("myBtn").addEventListener("click", addNewDocument);
//document.getElementById("showBtn").addEventListener("click", show);
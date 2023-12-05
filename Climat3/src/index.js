/*
DYLAN WILLIAMS FALL 2023
*/

//import from other files for readability and organization
import { DownloadXMLRDF } from "./downloadDocumentFunctions.js";
import { addNewDocument, loadJSONDocument } from "./addDocumentFunctions.js";
import { startSearch } from "./searchDocumentFunctions.js";

import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

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

console.log('Hello Firebase!'); //just to show it's working in console (fn f12 i think?)

//add listeners to the buttons needed

//this button will take the JSON file uploaded in databasetest.html, open the json, retrieve the data, and the input that data
//into documents in the database, into a collection defined by the user in databasetest.html
document.getElementById('uploadBtn').addEventListener('click', loadJSONDocument);

//this button is a simple test button to see how things work. it will get the collection name, document name, and the value of
//customer that the user defines in databasetest.html, and upload a document with that information into the database
document.getElementById("myBtn").addEventListener("click", addNewDocument);

//this button will go into the database with predetermined collection name and document names, retrieve the data for each of those
//documents, and format it into a Zotero RDF file that can then be uplaoded to Zotero
document.getElementById("openDocTest").addEventListener("click", DownloadXMLRDF);

//the search button, will look through the settings currently selected and perform the correct query, then outputs the data
document.getElementById("searchBtn").addEventListener("click", startSearch);


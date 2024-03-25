
import { initializeApp } from "firebase/app";
import { getFirestore, collection, query, where, getDocs, orderBy, startAt, endAt } from "firebase/firestore";
import { UpdateSelectedArray } from "./downloadDocumentFunctions.js";

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

var querySnapshot;
var pageNumber = 1;
var authorAll;

export async function startSearch() {
  //first start by setting up the query based on the preference of what the user selected to search by. current default is title
  var q;
  q = query(collection(db, "Documents"), orderBy('title'));

  //run the query, currently grabs all documents in the database
  querySnapshot = await getDocs(q);

  //initalize the amount of docs being displayed based off what the user picked. default is max of 20
  var maxPerPage = document.getElementById('resultsPerPage').value;
  showSearchResults(((maxPerPage * pageNumber) - maxPerPage), (maxPerPage * pageNumber));
}

export function pageUp() {
  pageNumber++;
  var maxPerPage = document.getElementById('resultsPerPage').value;
  showSearchResults(((maxPerPage * pageNumber) - maxPerPage), (maxPerPage * pageNumber))
}

export function pageDown() {
  if (pageNumber <= 1) {
    return;
  }
  pageNumber--;
  var maxPerPage = document.getElementById('resultsPerPage').value;
  showSearchResults(((maxPerPage * pageNumber) - maxPerPage), (maxPerPage * pageNumber))
}

function showSearchResults(minCountDocs, maxCountDocs) {
  //make sure the search has no card in it from a previous search
  const outputDiv = document.getElementById("output");
  outputDiv.innerHTML = '';
  var currentCountDocs = 0;
  //loop through all the documents in the query
  for (var i in querySnapshot.docs) {
    //if there is still more room for documents, proccess the documents
    if (currentCountDocs < maxCountDocs) {
      if (currentCountDocs < minCountDocs) {
        currentCountDocs++;
        continue;
      }
      const doc = querySnapshot.docs[i];

      //if the climate tag is specified, it will see if that document adheres to the tag, otherwise will go through all docs
      if (document.getElementById('sort-by-tag').value == 'All' || doc.data().ourTag == document.getElementById('sort-by-tag').value) {
        //checks if the document's title or author has the phrase the user is currently searching, and if so adds it to the page
        if (searchBy(doc)) {
          //if successful, increase the amount of docs currently on the page
          currentCountDocs++;
        }
      }
    } else {
      break;
    }
  }
}

//this function is mainly here to test the searchBy <select> tag to see what the user selected
function searchBy(doc) {
  //restart the current author string
  authorAll = "";
  
  //get all the keys of the current document and sort them
  var keys = Object.keys(doc.data()).sort();

  //for each key in the document, check if it is an author, and if so add it to the author list
  keys.forEach(function(key) {
      // Check if the variable starts with "author"
      if (key.startsWith("author_")) {
          if (doc.data()[key] !== undefined) {
              // Append data to the string if it exists
              authorAll += doc.data()[key];
              authorAll += ", ";
          }
      }
  });

  //searches the title and authors of each document, and if what the user searched is inluded, create a card for it
  if (doc.data().title.toLowerCase().includes(document.getElementById('searchText').value.toLowerCase()) ||
      authorAll.toLowerCase().includes(document.getElementById('searchText').value.toLowerCase())) {
    createCard(doc);
    return true;
  }
}

//where the actual card is created, this only appends one card to the bottom of the outputDiv
function createCard(doc) {
  //create a reference to the outputDiv
  const outputDiv = document.getElementById("output");

  //create a card Div to contain everything
  const cardDiv = document.createElement("div");
  cardDiv.classList.add("card");

  //create the header of the card with the title and a checkbox
  const cardHeaderDiv = document.createElement("div");
  cardHeaderDiv.classList.add("card-header");
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.addEventListener('change', UpdateSelectedArray);
  cardHeaderDiv.textContent = doc.data().title;
  cardHeaderDiv.appendChild(checkbox);

  //create a body of the card holding the author
  const cardBodyDiv = document.createElement("div");
  cardBodyDiv.classList.add("card-body");
  cardBodyDiv.textContent = authorAll;

  //create another body to hold the <a> tag that has the link provided for that document
  const cardBodyDiv2 = document.createElement("div");
  cardBodyDiv2.classList.add("card-body");
  const button = document.createElement("a");
  button.href = doc.data().url;
  button.classList.add("btn", "btn-primary");
  button.textContent = doc.data().url;
  cardBodyDiv2.appendChild(button);

  //append all the headers and bodys to the card, append the card to the ouptut div, then add a <p> tag for a little space between cards
  cardDiv.appendChild(cardHeaderDiv);
  cardDiv.appendChild(cardBodyDiv);
  cardDiv.appendChild(cardBodyDiv2);
  outputDiv.appendChild(cardDiv);
  outputDiv.appendChild(document.createElement("p"));

  //used only for debuggin/testing purposes
  console.log(doc.id, " => ", doc.data());
}
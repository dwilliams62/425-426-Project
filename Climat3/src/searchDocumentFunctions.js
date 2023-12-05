
import { initializeApp } from "firebase/app";
import { getFirestore, collection, query, where, getDocs, orderBy, startAt, endAt } from "firebase/firestore";

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

export async function startSearch() {
    const q = query(collection(db, "delete"), orderBy('title'), 
      startAt(document.getElementById('searchText').value), endAt(document.getElementById('searchText').value+'\uf8ff')); 
    const querySnapshot = await getDocs(q);
    const outputDiv = document.getElementById("output");
    outputDiv.innerHTML = '';
    console.log('tried');
    
    querySnapshot.forEach((doc) => {
      const cardDiv = document.createElement("div");
      cardDiv.classList.add("card");

      const cardHeaderDiv = document.createElement("div");
      cardHeaderDiv.classList.add("card-header");
      cardHeaderDiv.textContent = doc.data().title;

      const cardBodyDiv = document.createElement("div");
      cardBodyDiv.classList.add("card-body");
      cardBodyDiv.textContent = doc.data().author;

      const cardBodyDiv2 = document.createElement("div");
      cardBodyDiv2.classList.add("card-body");
      
      const button = document.createElement("a");
      button.href = doc.data().url;
      button.classList.add("btn", "btn-primary");
      button.textContent = doc.data().url;
      cardBodyDiv2.appendChild(button);

      cardDiv.appendChild(cardHeaderDiv);
      cardDiv.appendChild(cardBodyDiv);
      cardDiv.appendChild(cardBodyDiv2);
      outputDiv.appendChild(cardDiv);
      outputDiv.appendChild(document.createElement("p"));

      console.log(doc.id, " => ", doc.data());
    });
}
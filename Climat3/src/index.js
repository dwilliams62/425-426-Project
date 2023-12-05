/*
DYLAN WILLIAMS FALL 2023
*/

//import from other files for readability and organization
import { DownloadXMLRDF } from "./downloadDocumentFunctions.js";
import { addNewDocument, loadJSONDocument } from "./addDocumentFunctions.js";
import { } from "./searchDocumentFunctions.js";

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


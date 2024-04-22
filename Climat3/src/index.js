/*
DYLAN WILLIAMS SPRING 2024
*/

//import from other files for readability and organization
import { DownloadXMLRDF } from "./downloadDocumentFunctions.js";
import { startSearch, pageUp, pageDown, selectAllArticles, deselectAllArticles } from "./searchDocumentFunctions.js";

console.log('Hello Firebase!'); //just to show it's working in console (fn f12 i think?)

//add listeners to the buttons needed

//goes into the output div, finds the articles that the checkbox is checked, gets the title of those articles,
//and uses the titles to search the database for ids that equal it and download them into an XML RDF format
document.getElementById("downloadArticles").addEventListener("click", DownloadXMLRDF);

//the search button, will look through the settings currently selected and perform the correct query, then outputs the data to the output div
document.getElementById('search-button').addEventListener('click', startSearch);

//when the user hits page up or page down, shows more articles if there are any left to show
document.getElementById('pageUp').addEventListener('click', pageUp);
document.getElementById('pageDown').addEventListener('click', pageDown);

//either selects or deselects all checkboxes in the output div
document.getElementById('selectAll').addEventListener('click', selectAllArticles);
document.getElementById('deselectAll').addEventListener('click', deselectAllArticles);

//make sure the page starts with displaying some data based off the defaults picked when booted up
startSearch();


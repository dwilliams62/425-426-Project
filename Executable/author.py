from bs4 import BeautifulSoup  # pip install BeautifulSoup in terminal
import requests  # pip install requests in terminal
from itertools import zip_longest

URL = "https://pubmed.ncbi.nlm.nih.gov/9829131/"

page = requests.get(URL)

soup = BeautifulSoup(page.content,"html.parser")

authors = {}

auth = soup.find("div", class_="authors-list")



auth_elements = auth.find_all("a",class_="full-name")
link_elements = auth.find_all("a",class_="affiliation-link")

affiliations = soup.find("div", class_="affiliations")
aff_elements = affiliations.find_all("li")

keys =affiliations.find_all("sup",class_="key")
num = 1

for auth_element,link_element in zip_longest(auth_elements,link_elements): 
    a_elements = auth_element.text
    l_elements = link_element.text
    l_elements = int(l_elements)
    
    name = f'author_{num}'
    aff_name = f'affiliation_{num}'
    authors[name] = a_elements

    
    for aff_element, key in zip(aff_elements,keys): 
        aff = aff_element.text
        aff_key = key.text
        aff_key = int(aff_key)

        if aff_key == l_elements:
            authors[aff_name] = aff
            
    num += 1


for key, value in authors.items(): 
    print("key: ", key, " val:",value)
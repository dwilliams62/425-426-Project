from bs4 import BeautifulSoup  # pip install BeautifulSoup in terminal
import requests  # pip install requests in terminal
from itertools import zip_longest
import re

URL = "https://link.springer.com/article/10.1007/s10935-023-00750-2"

page = requests.get(URL)

soup = BeautifulSoup(page.content,"html.parser")

authors = {}

auth = soup.find("div",class_="c-article-header")

auth_elems = auth.find_all('a', attrs = {'data-test' : 'author-name'})

aff = soup.find("ol",class_="c-article-author-affiliation__list")
aff_elems = aff.find_all("p",class_="c-article-author-affiliation__address")
link_elems = aff.find_all("p",class_="c-article-author-affiliation__authors-list")



    
num = 1
for auth_elem in auth_elems: 
    a_elems = auth_elem.text.strip()
    
    
    author = re.sub(r'[0-9,]','',a_elems)
   # print(author)
    name = f'author_{num}'
    aff_name = f'affiliation_{num}'
    #check = f'check_{num}'
    authors[name] = author
    authors[aff_name] = ''

    for aff_elem, link_elem in zip(aff_elems, link_elems): 
        affiliations = aff_elem.text.strip()
        links = link_elem.text.strip()
       # print(links)
        final_aff = ''
        if author in links: 
            #authors[check] = "true"
            authors[aff_name] += affiliations
       
    num += 1
for key, value in authors.items(): 
    print("key: ", key, " val:",value)




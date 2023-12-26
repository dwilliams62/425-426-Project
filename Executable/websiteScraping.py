import re
from bs4 import BeautifulSoup  # pip install BeautifulSoup in terminal
import requests  # pip install requests in terminal

#scrapes pubmed, starts by going through the pages of articles, gets the url and title of each. then goes through each
#and scrapes the data needed and sets the array of dictionaries. the 5 things passed are the progress bar to update how
#how far it is, the amount of pages that should be scraped, the term to search by, the label that displays over the
#progress bar, and the root of the tkinter for forcing it to update 
def scrape_pubmed(progress_bar, page_count, scrape_term, pages_label, root):
    #start the array as empty, starts the label at what it needs to be
    array_of_articles = []
    pages_label.config(text="Opening...")

    #loop through the pages that need be scraped on pubmeds website
    for numbers in range(0, page_count):
        #configure the url for each page
        url = "https://pubmed.ncbi.nlm.nih.gov/?term={}&page={}".format(scrape_term, numbers)

        #open the url and make sure it was successful
        response = requests.get(url)
        if response.status_code == 200:
            #parse the data obtained with beautiful soup
            soup = BeautifulSoup(response.text, 'html.parser')
            texts = soup.find_all('a', class_="docsum-title")
            # Iterate through each article on the page and extract relevant information.
            for articles in texts:
                articles_text = articles.get_text()
                articles_text = articles_text.replace("\n", "")
                articles_text = re.sub(
                    r'(^[ \t]+|[ \t]+(?=:))', '', articles_text, flags=re.M)
                articles_links = articles.get('href')
                url = "https://pubmed.ncbi.nlm.nih.gov{0}".format(articles_links)
                #add a dicitonary for each article found, starting each with the correct url and title, and empty for each other info
                array_of_articles.append({"url":url, "title":articles_text, "itempType":"", "pubTitle":"", 
                    "pubYear":"", "author":"", "doi":"", "abstract":"", "date":"", "volume":"", "issue":"", "issn":"", 
                    "libCatalog":"", "manualTags":"", "autoTags":"", "ourTags":""})
                
        #update the progress bar to show how many pages have been checked
        progress_bar['value'] = (numbers/page_count) * 100
        root.update()
    
    #check how many articles are being scraped and update the label and progress bar accordingly
    numOfarticle = len(array_of_articles)
    progress = 100/numOfarticle
    progress_bar['value'] = 0
    pages_label.config(text="Scraping...")
    root.update()

    #loop through all the dictionaries in the array and update it with the information we scrape
    for article in array_of_articles:
        response = requests.get(article['url'])
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            abstract = soup.find('div', class_="abstract-content selected")
            if abstract == None:
                print("This article does not an abstract:", article['title'])
            else:
                article["itemType"] = "journalArticle"
                article["title"] = article

                # Find the publication title for the article.
                # If no publication title is found, print a message and set the publication title to an empty string.
                Pubtitles = soup.find('p', class_='literature-footer-text')
                if Pubtitles == None:
                    print("No Publication Title for", article['title'])
                    article['pubTitle'] = ""
                else:
                    article['pubTitle'] = Pubtitles.get_text()

                # Find the authors for the article.
                # If no authors are found, print a message and set the authors to an empty string.
                authors_PMED = soup.find('div', class_="authors-list")
                if authors_PMED == None:
                    print("No Author for", article['title'])
                    article['author'] = ""
                else:
                    authors_name = ''
                    keylist = []
                    for authors in authors_PMED.find_all('a', class_="full-name"):
                        author_names = authors.get_text()
                        author_names = author_names.encode(
                            "ascii", 'ignore')
                        author_names = author_names.decode()
                        author_names = author_names.replace(
                            "\n", '')
                        author_names = re.sub(
                            r'(^[ \t]+|[ \t]+(?=:))', '', author_names, flags=re.M)
                        keylist.append(author_names)
                    authors_name = authors_name + ", ".join(keylist)
                    article['author'] = authors_name

                # Find the publication year for the article.
                # If no publication year is found, print a message and set the publication year to an empty string.
                PUBYear = soup.find('span', class_='cit')
                if PUBYear == None:
                    print("No publication year for: ", article['title'])
                    article["pubYear"] = ""
                else:
                    public_year = PUBYear.get_text()
                    public_year = public_year.split(" ")[0]
                    article["pubYear"] = public_year

                # Find the DOI (Digital Object Identifier) for the article.
                # If no DOI is found, print a message and set the DOI to an empty string.
                DOI = soup.find('a', class_='id-link',attrs={"data-ga-action": 'DOI'})
                if DOI == None:
                    print("No DOI for: ", article['title'])
                    article["doi"] = ""
                else:
                    doi_text = DOI.get_text()
                    doi_text = re.sub(
                        r'(^[ \t]+|[ \t]+(?=:))', '', doi_text, flags=re.M)
                    doi_text = doi_text.replace('\n', "")
                    article["doi"] = doi_text

                # Find the abstract for the article.
                # If no abstract is found, print a message and set the abstract to an empty string.
                abstract = soup.find('div', class_="abstract-content selected")
                if abstract == None:
                    print("No Abstract for: ", article['title'])
                    article["abstract"] = ""
                else:
                    abs = abstract.get_text()
                    abs = abs.replace("\n", "")
                    abs = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', abs, flags=re.M)
                    article["abstract"] = abs
                
                # Find the date of the article.
                # If no date is found, print a message and set the date to an empty string.
                date = soup.find('span', class_='cit')
                if date == None:
                    print("No Date for: ", article['title'])
                    article['date'] = ""
                else:
                    date_text = date.get_text()
                    date_text = date_text.split(";")[0]
                    article['date'] = date_text

                # Find the volume of the article.
                # If no volume is found, print a message and set the volume to an empty string.
                volume = soup.find('span', class_='cit')
                if volume == None:
                    print("No Volume for: ", article['title'])
                    article['volume'] = ""
                else:
                    try: 
                        vol_text = volume.get_text()
                        vol_text = vol_text.split(";")[1]
                        vol_text = vol_text.split("(")[0]
                        article["volume"] = vol_text
                    except IndexError:
                        print("Error with Volume")

                # Find the ISSN of the article.
                # If no ISSN is found, print a message and set the ISSN to an empty string.
                issn = soup.find('span', class_='cit')
                if issn == None:
                    print("No ISSN for: ", article['title'])
                    article['issn'] = ""
                else:
                    try: 
                        ISSN_text = issn.get_text()
                        ISSN_text = ISSN_text.split(":")[0]
                        ISSN_text = ISSN_text.split(";")[1]
                        ISSN_text = ISSN_text.split(")")[0]
                        try:
                            ISSN_text.split("(")[1]
                        except IndexError:
                            ISSN_text = ISSN_text.split(":")[0]
                        else:
                            ISSN_text = ISSN_text.split("(")[1]
                        article["issn"] = ISSN_text
                    except IndexError:
                        try:
                            ISSN_text = issn.get_text()
                            ISSN_text = ISSN_text.split(":")[0]
                            ISSN_text = ISSN_text.split(":")[1]
                            ISSN_text = ISSN_text.split(")")[0]
                        except IndexError: 
                            print("Error on ISSN")
                            article["issn"] = ""
                        else:
                            try:
                                ISSN_text.split("(")[1]
                            except IndexError:
                                ISSN_text = ISSN_text.split(":")[0]
                                article["issn"] = ISSN_text
                            else:
                                ISSN_text = ISSN_text.split("(")[1]
                                article["issn"] = ISSN_text

                # Set the library catalog to "PubMed" for the article.
                article["libCatalog"] = "PubMed"

                # Set these things to empty
                article["issue"] = ""
                article["manualTags"] = ""
                article["autoTags"] = ""
                article["ourtags"] = ""

        #update the progress bar
        progress_bar['value'] += progress
        root.update()
     
    #create a copy and loop through, and if the article doesn't have an abstract, remove it from the array
    array_copy = array_of_articles
    for article in array_copy:
        if article['abstract'] == "":
            array_of_articles.remove(article)

    return array_of_articles


def scrape_springer(progress_bar, page_count, scrape_term, pages_label, root):
    progress_bar['value'] = page_count

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
    for numbers in range(0, page_count+1):
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
                array_of_articles.append({"url":url, "title":articles_text})
                
        #update the progress bar to show how many pages have been checked
        progress_bar['value'] = (numbers/(page_count+1)) * 100
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
                article["title"] = article['title']

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
                article["ourTags"] = ""

        #update the progress bar
        progress_bar['value'] += progress
        root.update()
     
    #create a copy and loop through, and if the article doesn't have an abstract, remove it from the array
    filtered_articles = [article for article in array_of_articles if article.get('abstract') != "None"]

    return filtered_articles



#the basics of springer scraping is the same as the pubmed scraping
def scrape_springer(progress_bar, page_count, scrape_term, pages_label, root):
    #start the array as empty, starts the label at what it needs to be
    array_of_articles = []
    pages_label.config(text="Opening...")

    #loop through the pages that need be scraped on pubmeds website
    for numbers in range(0, page_count):
        #configure the url for each page
        url = "https://link.springer.com/search/page/{}?query={}&facet-content-type=%22Article%22".format(numbers,scrape_term)

        #open the url and make sure it was successful
        response = requests.get(url)
        if response.status_code == 200:
            #parse the data obtained with beautiful soup
            soup = BeautifulSoup(response.text, 'html.parser')
            texts = soup.find_all('a', class_ = "title")
            # Iterate through each article on the page and extract relevant information.
            for articles in texts:
                articles_text = articles.get_text()
                articles_links = articles.get('href')
                url = "https://link.springer.com{}".format(articles_links)
                #add a dicitonary for each article found, starting each with the correct url and title, and empty for each other info
                array_of_articles.append({"url":url, "title":articles_text, "itempType":"", "pubTitle":"", 
                    "pubYear":"", "author":"", "doi":"", "abstract":"None", "date":"", "volume":"", "issue":"", "issn":"", 
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
            print("Successfully opened the web page \n")
            # accessing the hmtl of the the website
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract article details.
            abstract = soup.find('div', class_="main-content")
            # Check if an abstract is available.
            if abstract == None:
                print("This article does not an abstract:", article['title'])
            else:
                # Extract article information and format accordingly.
                article["itemType"] = "journalArticle"
                article_name = article['title'].encode("ascii", 'ignore')
                article_name = article_name.decode()
                article["title"] = article_name
                # Extract other article information similarly.
                Pubtitles = soup.find('i', attrs = {'data-test': 'journal-title'})
                if Pubtitles == None:
                    print("No Publication Title for", articles)
                    article['pubTitle'] = ""
                else:
                    article['pubTitle'] = Pubtitles.get_text()
                # Extract authors names
                authors = soup.find_all('a', attrs = {'data-test' : 'author-name'})
                if authors == None:
                    print("No Author for", articles)
                    article['author'] = ""
                else:
                    authors_name = ''
                    keylist = []
                    for authors in authors:
                        author_names = authors.get_text()
                        author_names = author_names.encode("ascii", 'ignore')
                        author_names = author_names.decode()
                        author_names = author_names.replace( "\n", '')
                        author_names = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', author_names, flags=re.M)
                        keylist.append(author_names)
                    authors_name = authors_name + ", ".join(keylist)
                    article['author'] = authors_name
                # Extract publication year
                PUBYear = soup.find('span', class_  = 'c-bibliographic-information__value')
                if PUBYear == None:
                    print("No publication year for: ", articles)
                    article["pubYear"] = ""
                else:
                    try:
                        public_year = PUBYear.get_text()
                        public_year = public_year.split(" ")[2]
                        article["pubYear"] = public_year
                    except IndexError:
                        print("error with pub year")
                # Extract DOI
                DOI = soup.find('li', class_="c-bibliographic-information__list-item c-bibliographic-information__list-item--doi")
                if DOI == None:
                    print("No DOI for: ", articles)
                    article["doi"] = ""
                else:
                    for doi in DOI.find('span', class_ = 'c-bibliographic-information__value'):
                        doi_text = doi.get_text()
                        doi_text = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', doi_text, flags=re.M)
                        doi_text = doi_text.replace('\n', "")
                    article["doi"] = doi_text
                # Extract URL
                article["url"] = url
                # Extract abstract
                abstract = soup.find('div', class_="main-content")
                if abstract == None:
                    print("No Abstract for: ", articles)
                    article["abstract"] = ""
                else:
                    abs = " "
                    for springer_abstract in abstract.find_all('p'):
                        abs += springer_abstract.get_text()
                        abs = abs.replace("\n", "")
                        abs = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', abs, flags=re.M)
                        abs = abs.encode("ascii", 'ignore')
                        abs = abs.decode()
                    article["abstract"] = abs
                # Extract date, volume, and other information
                date = soup.find('span', class_='c-bibliographic-information__value')
                if date == None:
                    print("No Date for: ", articles)
                    article['date'] = ""
                else:
                    date_text = date.get_text()
                    article['date'] = date_text
                volume = soup.find('p', class_='c-bibliographic-information__citation')
                if volume == None:
                    print("No Volume for: ", articles)
                    article['volume'] = ""
                else:
                    try: 
                        for vol in volume.find('b'):
                            vol_text = vol.get_text()
                        
                    except TypeError:
                        print("Error on volume")
                article["volume"] = vol_text
                
                # Initialize other fields with empty values
                article["issue"] = ""
                article['issn'] = ""
                article["libCatalog"] = "Springer"
                article["manualTags"] = ""
                article["autoTags"] = ""
                article["ourTags"] = ""

        #update the progress bar
        progress_bar['value'] += progress
        root.update()
     
    #create a copy and loop through, and if the article doesn't have an abstract, remove it from the array
    filtered_articles = [article for article in array_of_articles if article.get('abstract') != "None"]

    return filtered_articles
import re
from bs4 import BeautifulSoup  # pip install BeautifulSoup in terminal
import requests  # pip install requests in terminal
from itertools import zip_longest

#scrapes pubmed, starts by going through the pages of articles, gets the url and title of each. then goes through each
#and scrapes the data needed and sets the array of dictionaries. the 5 things passed are the progress bar to update how
#how far it is, the amount of pages that should be scraped, the term to search by, the label that displays over the
#progress bar, and the root of the tkinter for forcing it to update 
def scrape_pubmed(progress_bar, page_start, page_end, scrape_term, pages_label, root):
    #start the array as empty, starts the label at what it needs to be
    array_of_articles = []
    pages_label.config(text="Opening...")
    page_start = int(page_start)
    page_end = int(page_end)
    if page_start == 1: 
        page_start = 0
        #if page_end == 1: 
            #page_end = 0

    #loop through the pages that need be scraped on pubmeds website
    for numbers in range(page_start, page_end+1):
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
                    "pubYear":"",  "doi":"", "abstract":"None", "date":"", "volume":"", "issue":"", "issn":"", 
                    "libCatalog":"", "manualTags":"", "autoTags":"", "ourTags":"","keywords":""})
                
        #update the progress bar to show how many pages have been checked
        page_count = 0; 
        if page_start == page_end: 
            page_count = 1
        else: 
            page_count = (page_end - page_start)+1
        progress_bar['value'] = (numbers/(page_count+1)) * 100
        root.update()
    
    #check how many articles are being scraped and update the label and progress bar accordingly
    try: 
        numOfarticle = len(array_of_articles)
        progress = 100/numOfarticle
        progress_bar['value'] = 0
    except ZeroDivisionError as e :
        return None,None,str(e)
    
    pages_label.config(text="Scraping...")
    root.update()

    #Value to keep and calculate the accuracy of the scraper
    fields_needed = 11
    percentages = {"percentage":0}
   

    


    #loop through all the dictionaries in the array and update it with the information we scrape
    for article in array_of_articles:
       
        
        #Value that checks to see how many fields were not scraped due to bad data
        missing_fields = 0
        accuracy = 0
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
                    missing_fields += 1
                else:
                    article['pubTitle'] = Pubtitles.get_text()

                # Find the authors for the article and their affiliated affilaiation.
                # If no authors are found, print a message and set the authors to an empty string.
                # If no affiliation is found prints no affiliation and only add author names to dictionary
                auth = soup.find('div', class_="authors-list")
                if auth == None:
                    print("No Author for", article['title'])
                    article['author'] = ""
                    missing_fields += 1
                else:                    
                    auth_elements = auth.find_all("a",class_="full-name")
                    link_elements = auth.find_all("a",class_="affiliation-link")
                    

                    affiliations = soup.find("div", class_="affiliations")
                    # this checks if the article has author affiliations
                    try:
                        aff_elements = affiliations.find_all("li")
                        keys =affiliations.find_all("sup",class_="key")
                    except AttributeError: 
                        # If there are no affiliations add the author names only
                        print("No Affiliations for: ", article['title'])
                        missing_fields += 1
                        num = 1
                    
                        for auth_element in auth_elements:
                            
                            a_elements = auth_element.text
                            name = f'author_{num}'
                            article[name] = a_elements
                            num += 1
                                            
                    num = 1
                    # goes through the website to find every author and their affiliation link and finds their corresponding
                    # affiliation by matching to the affiliation key
                    for auth_element,link_element in zip(auth_elements,link_elements): 
                        a_elements = auth_element.text
                        
                        l_elements = link_element.text
                        l_elements = int(l_elements)
    
                        name = f'author_{num}'
                        aff_name = f'affiliation_{num}'
                        article[name] = a_elements

                        if aff_elements != None:
                            for aff_element, key in zip(aff_elements,keys): 
                                aff = aff_element.text
                                aff_key = key.text
                                aff_key = int(aff_key)

                                if aff_key == l_elements:
                                    article[aff_name] = aff
            
                        num += 1


                # Find the publication year for the article.
                # If no publication year is found, print a message and set the publication year to an empty string.
                PUBYear = soup.find('span', class_='cit')
                if PUBYear == None:
                    print("No publication year for: ", article['title'])
                    article["pubYear"] = ""
                    missing_fields += 1
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
                    missing_fields += 1
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
                    missing_fields += 1
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
                    missing_fields += 1
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
                    missing_fields += 1
                else:
                    try: 
                        vol_text = volume.get_text()
                        vol_text = vol_text.split(";")[1]
                        vol_text = vol_text.split("(")[0]
                        article["volume"] = vol_text
                    except IndexError:
                        missing_fields += 1
                        print("Error with Volume")

                # Find the ISSN of the article.
                # If no ISSN is found, print a message and set the ISSN to an empty string.
                issue = soup.find('span', class_='cit')
                if issue == None:
                    print("No issue for: ", article['title'])
                    article['issue'] = ""
                    missing_fields += 1
                else:
                    try: 
                        ISSUE_text = issue.get_text()
                        ISSUE_text = ISSUE_text.split(":")[0]
                        ISSUE_text = ISSUE_text.split(";")[1]
                        ISSUE_text = ISSUE_text.split(")")[0]
                        try:
                            ISSUE_text.split("(")[1]
                        except IndexError:
                            ISSUE_text = ISSUE_text.split(":")[0]
                        else:
                            ISSUE_text = ISSUE_text.split("(")[1]
                        article["issue"] = ISSUE_text
                    except IndexError:
                        try:
                            ISSUE_text = issue.get_text()
                            ISSUE_text = ISSUE_text.split(":")[0]
                            ISSUE_text = ISSUE_text.split(":")[1]
                            ISSUE_text = ISSUE_text.split(")")[0]
                        except IndexError: 
                            print("Error on ISSUE")
                            article["issue"] = ""
                            missing_fields += 1
                        else:
                            try:
                                ISSUE_text.split(")")[1]
                            except IndexError:
                                ISSUE_text = ISSUE_text.split(":")[0]
                                article["issue"] = ISSUE_text
                            else:
                                ISSUE_text = ISSUE_text.split("(")[1]
                                article["issue"] = ISSUE_text
                
                #Parse for ISSN 
                issn = soup.find('span', class_='cit')
                if issn == None:
                    print("No issn for: ", article['title'])
                    article['issn'] = ""
                    missing_fields += 1
                else: 
                    try: 
                        ISSN_text = issn.get_text()
                        ISSN_text = ISSN_text.split(":")[1]
                        ISSN_text = ISSN_text.split(".")[0]
                    except IndexError: 
                        print("error on ISSN for: ",article['title'])
                        article["issn"] = ""
                        missing_fields += 1
                    else: 
                        article["issn"] = ISSN_text
                
            #Adding key terms if they exist 
                keys = soup.find("div",class_="abstract")
                keywords =keys.find_all("p")

                if keywords == None:
                    article["keywords"] = " "
                    print("Error on keywords for: ",article['title'])
                    missing_fields += 1
                else: 
                    
                    for keyword in keywords:
                        keywords_text = keyword.get_text()
                        if 'Keywords:' not in keywords_text:
                            article["keywords"] = " "
                            print("Error on keywords for: ",article['title'])
                            
                                                       
                        else: 
                            keywords_text = keywords_text.split(":")[1]
                            keywords_text = keywords_text.strip()
                            article["keywords"] = keywords_text
                            print(article["keywords"])
                    if article["keywords"] == " ":
                        missing_fields +=1
                            
                print("this is the number of missign fields : ", missing_fields)
                accuracy = missing_fields / fields_needed 
                print("this is the accuracy: ", accuracy)
                percentages["percentage"] += accuracy
                print("this is the cumulative", percentages["percentage"])


                # Set the library catalog to "PubMed" for the article.
                article["libCatalog"] = "PubMed"

                # Set these things to empty
                #article["issn"] = ""
                article["manualTags"] = ""
                article["autoTags"] = ""
                article["ourTags"] = ""

        #update the progress bar
        progress_bar['value'] += progress
        
        root.update()
 
 
    calculation = (percentages['percentage'] / numOfarticle)*100
    rounded_calc =round(calculation,2)
    

    print("The percentage of missing data for this scraping is : ", rounded_calc)
    
    #create a copy and loop through, and if the article doesn't have an abstract, remove it from the array
    filtered_articles = [article for article in array_of_articles if article.get('abstract') != "None"]

    return filtered_articles,rounded_calc, None



#the basics of springer scraping is the same as the pubmed scraping
def scrape_springer(progress_bar,page_start,page_end, scrape_term, pages_label, root):
    #start the array as empty, starts the label at what it needs to be
    array_of_articles = []
    pages_label.config(text="Opening...")
    page_start = int(page_start)
    page_end = int(page_end)

    if page_start == 1:
        page_start = 0

    #loop through the pages that need be scraped on pubmeds website
    for numbers in range(page_start, page_end+1):
        #configure the url for each page
        url = "https://link.springer.com/search/page/{}?query={}&facet-content-type=%22Article%22&showAll=false".format(numbers,scrape_term)

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
        page_count = 0; 
        if page_start == page_end: 
            page_count = 1
        else: 
            page_count = (page_end - page_start)+1
        
        progress_bar['value'] = (numbers/page_count) * 100
        root.update()
    
    #check how many articles are being scraped and update the label and progress bar accordingly
    try:
        numOfarticle = len(array_of_articles)
        progress = 100/numOfarticle
    except ZeroDivisionError as e :
        return None,None,str(e)
    progress_bar['value'] = 0
    pages_label.config(text="Scraping...")
    root.update()
# this is to calculate how many different fields that we need a
    fields_needed = 10
    percentages = {"percentage":0}

    #loop through all the dictionaries in the array and update it with the information we scrape
    for article in array_of_articles:
         #Value that checks to see how many fields were not scraped due to bad data
        missing_fields = 0
        accuracy = 0
        response = requests.get(article['url'])
        if response.status_code == 200:
            print("Successfully opened the web page \n")
            # accessing the hmtl of the the website
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract article details.
            abstract = soup.find('div', class_="main-content")
            # Check if an abstract is available.
            if abstract == None or abstract.text == '':
                abstract == None
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
                    print("No Publication Title for", article['title'])
                    article['pubTitle'] = ""
                    missing_fields += 1
                else:
                    article['pubTitle'] = Pubtitles.get_text()
                # Extract authors names and the author affiliations
                auth = soup.find("div",class_="c-article-header")
               

                auth_elems = auth.find_all('a', attrs = {'data-test' : 'author-name'})
                if auth_elems == None:
                    print("No Author for", article['title'])
                    article['author'] = ""
                    missing_fields += 1
                else:
                    # authors_name = ''
                    # keylist = []
                    # for authors in authors:
                    #     author_names = authors.get_text()
                    #     author_names = author_names.encode("ascii", 'ignore')
                    #     author_names = author_names.decode()
                    #     author_names = author_names.replace( "\n", '')
                    #     author_names = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', author_names, flags=re.M)
                    #     keylist.append(author_names)
                    # authors_name = authors_name + ", ".join(keylist)
                    # article['author'] = authors_name
                    
                    aff = soup.find("ol",class_="c-article-author-affiliation__list")

                    if aff == None : 
                        print("NO affiliations for ", article['title'])
                        num = 1
                        missing_fields += 1
                        for auth_elem in auth_elems: 
                            a_elems = auth_elem.text.strip()

                            author = re.sub(r'[0-9,]','',a_elems)
                            
                            name = f'author_{num}'
                            aff_name = f'affiliation_{num}'                            
                            article[name] = author
                            article[aff_name] = ''
                        num += 1
                    else:
                        aff_elems = aff.find_all("p",class_="c-article-author-affiliation__address")
                        link_elems = aff.find_all("p",class_="c-article-author-affiliation__authors-list")

                        num = 1
                        for auth_elem in auth_elems: 
                            a_elems = auth_elem.text.strip()

                            author = re.sub(r'[0-9,]','',a_elems)
                            
                            name = f'author_{num}'
                            aff_name = f'affiliation_{num}'
                            
                            article[name] = author
                            article[aff_name] = ''

                            for aff_elem, link_elem in zip(aff_elems, link_elems): 
                                affiliations = aff_elem.text.strip()
                                links = link_elem.text.strip()
                                if author in links: 
                                    article[aff_name] += affiliations
                            num += 1
                # Extract publication year
                PUBYear = soup.find('span', class_  = 'c-bibliographic-information__value')
                if PUBYear == None:
                    print("No publication year for: ", article['title'])
                    article["pubYear"] = ""
                    missing_fields += 1
                else:
                    try:
                        public_year = PUBYear.get_text()
                        public_year = public_year.split(" ")[2]
                        article["pubYear"] = public_year
                    except IndexError:
                        print("error with pub year")
                        missing_fields += 1
                # Extract DOI
                DOI = soup.find('li', class_="c-bibliographic-information__list-item c-bibliographic-information__list-item--doi")
                if DOI == None:
                    print("No DOI for: ", article['title'])
                    article["doi"] = ""
                    missing_fields += 1
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
                if abstract == None :
                    print("No Abstract for: ", article['title'])
                    article["abstract"] = ""
                    missing_fields += 1
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
                    print("No Date for: ", article['title'])
                    article['date'] = ""
                    missing_fields += 1
                else:
                    date_text = date.get_text()
                    article['date'] = date_text
                volume = soup.find('p', class_='c-bibliographic-information__citation')
                if volume == None:
                    print("No Volume for: ", article['title'])
                    article['volume'] = ""
                    missing_fields += 1
                else:
                    try: 
                        for vol in volume.find('b'):
                            vol_text = vol.get_text()
                        
                    except TypeError:
                        print("Error on volume")
                        missing_fields += 1
                article["volume"] = vol_text

                accuracy = missing_fields / fields_needed 
                print("this is the accuracy: ", accuracy)
                percentages["percentage"] += accuracy
                print("this is the cumulative", percentages["percentage"])
                
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
    
    calculation = (percentages['percentage'] / numOfarticle)*100
    rounded_calc =round(calculation,2)
    

    print("The percentage of missing data for this scraping is : ", rounded_calc)
     
    #create a copy and loop through, and if the article doesn't have an abstract, remove it from the array
    filtered_articles = [article for article in array_of_articles if article.get('abstract') != "None"]

    return filtered_articles,rounded_calc, None
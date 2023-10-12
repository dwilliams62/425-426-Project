from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient  # to connect to the database
import yaml  # to connect to database
import certifi  # to connect to database
import math
import re
import threading
import os
from bs4 import BeautifulSoup  # pip install BeautifulSoup in terminal
import requests  # pip install requests in terminal
import webbrowser  # allow to open a website
# allow the program to use findall word in a string ignoring spaces and puting it in a list.
import json  # Json libary allow the text file to covert to a json file
running = True  # Global flag
# To connect to the Mongo DB database run these line of code  within the multiple ### line also import yaml, certifi, from pymongo import MongoClient
#######################################################################
config = yaml.safe_load(open('db.yaml'))

try:
     client = MongoClient(config['uri'], tlsCAFile = certifi.where())
     print("\nSuccessful connection.\n")
except:
     print("\nUnsuccessful connection.\n")

db = client['biomez']
collection = db.raw_records

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Biome-Z GUI")
        self.geometry("1150x500")
        tabControl = ttk.Notebook(self)
        self.tab2 = ttk.Frame(tabControl)
        tabControl.add(self.tab2, text="Mannual")
        self.tab3 = ttk.Frame(tabControl)
        tabControl.add(self.tab3, text="WEB-Scrape")
        tabControl.pack(expand=1, fill="both")

        self.addingWidgets()

    def addingWidgets(self):
        articles_list = []
        file = open("Articles.json", "x", encoding="utf-8")
        file.write(json.dumps(articles_list))

        def update(data):
            List_box.delete(0, END)
            # add articles to Listbox
            for item in data:
                List_box.insert(END, item)

        def fillout(e):
            # Delete whatever is in the entry box
            Article_input.delete(0, END)
            # add clicked list item to entry box
            Article_input.insert(0, List_box.get(ANCHOR))
        message = '''
User Mannual Webscraper: 
Tab WEB-Scrape:
    websites: Nature, PubMed, Springer (These are the website that can be chosen for articles information to be scrape on to a Json file)

    After a website is chosen, input a search term (for example use the term Microbiome) in to the search bar then click the enter button.
    
    Click the enter button on the right side of the search bar. A horizontal scorll will appear and it will allow the scraper to Generate/Web 
    scrape multiple 
    articles within the pages. Choose the number of pages.
    
    Generate Articles button:
        By clicking the Generate Articles button, all the article related to the search term will be show in the list-box on the right side
        Viewing article web pages:
            Once the article are shown in the list box, any one of the article show in the list-box can be view on their web page by click on
            the name of the article and then clicking on the View Article button.
    Scrape-by-term button:
        by clicking the Scrape-by-term button, all the article related to the search term and scrape the information 
        (titles, author name, publication, date, doi, etc) of that articles and place it in a Json file.
        A progess bar will appear to show to progress of all the article having their info scrape into a Json file 
        
    Upload to Mongo DB-database button:
        After all the article information have been scrape and place into the Json file called Articles.json. 
        Clicking Upload to Mongo DB-database button will upload the json file with the article info to the raw_records 
        database hosted by MongoDB.
     '''
    
        #Create a Text widget for displaying a message in a tab.
        Mannual_box = Text(self.tab2, height=29, width=145, bg="lightgray" )
        Mannual_box.insert('end', message)
        Mannual_box.pack(expand=True)
        Mannual_box.config(state='disabled')

        #Define variables for website links.
        wedsite_linkButton3 = StringVar()
        wedsite_linkButton = StringVar()
        wedsite_linkButton2 = StringVar()

        #Create a labeled frame for website selection.
        labelFrame4 = ttk.LabelFrame(
            self.tab3, text="Website:", width=400, height=50)
        labelFrame4.pack(side=LEFT, anchor="n")

        #Create buttons for different websites and set their properties.
        NatureButton = Button(labelFrame4, textvariable=wedsite_linkButton,
                              command=lambda: article_search_natural(), font=("TkHeadingFont", 12), width=10)

        #Set the button text for Nature
        wedsite_linkButton.set("Nature")
        NatureButton.place(y=0, x=0)
        PUBMButton = Button(labelFrame4, textvariable=wedsite_linkButton2, command=lambda: article_search_PUBMED(), font=(
            "TkHeadingFont", 12), width=10)
        #Set the button text for Nature
        wedsite_linkButton2.set("PubMed")
        PUBMButton.place(y=0, x=150)
        wedsite_linkButton3 = StringVar()
        SpringerButton = Button(labelFrame4, textvariable=wedsite_linkButton3, command=lambda: article_search_Springer(),font=(
            "TkHeadingFont", 12), width=10)
        wedsite_linkButton3.set("Springer")
        SpringerButton.place(y=0, x=295)

        # Define a labeled frame for article search and related elements.
        labelFrame6 = ttk.LabelFrame(
            self.tab3, text="Article Search:", width=670, height=475)
        labelFrame6.place(x=470)

        # Create labels, input fields, and a listbox for article search.
        Art_label = Label(labelFrame6, text="Choose article: ",
                          font=("TkHeadingFont", 12))
        Art_label.place(y=6)
        Article_input = Entry(labelFrame6, font=(
            "TkHeadingFont", 12), width=73)
        Article_input.place(y=35)
        List_box = Listbox(labelFrame6, font=(
            "TkHeadingFont", 13), height=19, width=73)
        List_box.place(y=70)

        # Bind a function to the listbox selection event.
        List_box.bind("<<ListboxSelect>>", fillout)

        # Define a function for searching articles on the 'Nature' website.
        def article_search_natural():
            # Create a labeled frame for the search term input and buttons
            labelFrame5 = ttk.LabelFrame(
            self.tab3, text="Search Term for Nature:", width=400, height=190)
            labelFrame5.place(y=80)
            # Create input fields and buttons for searching articles by term on 'Nature'.
            search_term = Label(
                labelFrame5, text="Input term:", font=("TkHeadingFont", 12))
            search_term.place(y=25)
            # Entry field for the search term
            Term_searchbox = Entry(labelFrame5, font=("TkHeadingFont", 12), width=27)
            Term_searchbox.place(y=25, x=90)
            # Button to initiate search and enter page selection
            search_pages = Button(labelFrame5, text="Enter", command=lambda:  page_num(), font=("TkHeadingFont", 10), width=5)
            search_pages.place(y=22, x=345)
            
            # Define a function for handling the page number input and initiating article generation.
            def page_num():
                # Create a button to generate articles by calling the generate_articles_natural function
                Gen_articles = Button(labelFrame5, text="Generate articles", command=lambda:  threading.Thread(
                    target= generate_articles_natural).start(), font=("TkHeadingFont", 12), width=14)
                Gen_articles.place(y=135)
                # Create a button to initiate web scraping by term using ScrapeArticle_bytermNatural function
                Webscrape_byterm = Button(labelFrame5, text="Scrape by term",  command=lambda:  threading.Thread(target= ScrapeArticle_bytermNatural).start(),font=("TkHeadingFont", 12), width=14)
                Webscrape_byterm.place(x=260, y=135)
                # Get the search term from the Term_searchbox
                term = Term_searchbox.get()
                url = "https://www.nature.com/search?q={}".format(term)# Construct the URL for the search term
                response = requests.get(url)# Send a request to the URL
                # Check if the response status code is 200 (success)
                if response.status_code == 200:
                    print("Successfully opened the web page \n")
                    pages = 20 # Set the maximum number of pages to scrape
                # Create a slider (Scale) to select the number of pages to scrape    
                page_Scaler = Scale(labelFrame5, from_=0,
                                    to=pages, orient=HORIZONTAL, length=285)
                page_Scaler.place(y=75, x=100)
                # Display a label indicating the number of pages
                Pages = Label(labelFrame5, text='# of pages:',
                              font=("TkHeadingFont", 12))
                Pages.place(y=90)

                #Define a function for generating articles based on the search term
                def generate_articles_natural():
                    dicts = {}# Dictionary to store article titles and links
                    Article_list = []# List to store article titles
                    term = Term_searchbox.get()# Get the search term from a search box
                    # Loop through the specified number of pages
                    for numbers in range(0, page_Scaler.get()+1):
                        # Construct the URL for the search term and page number
                        url = "https://www.nature.com/search?q={}&page={}".format(term,numbers)
                        response = requests.get(url)# Send a request to the URL
                        # Check if the response status code is 200 (success)
                        if response.status_code == 200:
                            print("Successfully opened the web page \n")
                            soup = BeautifulSoup(response.text, 'html.parser')
                            texts = soup.find_all('a', class_="c-card__link u-link-inherit")
                            # Iterate through the found articles and extract their titles and links
                            for articles in texts:
                                articles_text = articles.get_text()
                                articles_links = articles.get('href')
                                dicts[articles_text] = articles_links

                    # Iterate through the keys in the dictionary and append article titles to the Article_list            
                    for key in dicts.keys():
                        Article_list.append(key)

                    # Update the view with the list of articles    
                    update(Article_list)

                    # Create a button to view an article
                    View_Art = Button(labelFrame6, text="View Article", font=(
                        "TkHeadingFont", 11), command=lambda: view_article(), width=13)
                    View_Art.place(y=0, x=535)

                    #Defined function to view articles from nature.com
                    def view_article():
                        article = Article_input.get()#gets the selected article
                        webbrowser.open("https://www.nature.com{0}".format(dicts[article]))#This opens the corresponding article

                #Define a function for scraping articles by term "Nature".
                def ScrapeArticle_bytermNatural():
                    dicts = {}
                    Article_list = []
                    articles_dicts = {}
                    article_dicts = {}
                    #Get the search term from the input box
                    term = Term_searchbox.get()
                    #Iterate over the specified range of pages to scrape articles.
                    for number in range(1, page_Scaler.get()+1):
                        #Construct the URL for the current page.
                        url = "https://www.nature.com/search?q={}&page={}".format(term,number)
                        response = requests.get(url)
                        #Check if the web page was successfully accessed
                        if response.status_code == 200:
                            print("Successfully opened the web page \n")
                            #Parse the HTML content of the page.
                            soup = BeautifulSoup(response.text, 'html.parser')
                            #Find all article links on the page
                            texts = soup.find_all('a', class_="c-card__link u-link-inherit")
                            #Store article titles and links in a dictionary
                            for articles in texts:
                                articles_text = articles.get_text()
                                articles_links = articles.get('href')
                                dicts[articles_text] = articles_links
                    #Store article titles in a list
                    for key in dicts.keys():
                        Article_list.append(key)
                    #Create a labeled frame for the progress bar and related elements
                    labelFrame7 = ttk.LabelFrame(self.tab3, text="Articles scraping progress bar: ", width=400, height=140)
                    labelFrame7.place(y=315)
                    articles_progress = ttk.Progressbar(labelFrame7, orient=HORIZONTAL, length= 395, mode='determinate')
                    articles_progress.place(y=30)
                    progress_label = Label(labelFrame7, text="")
                    precent_label = Label(labelFrame7, text="%")
                    precent_label.place(y=55, x=186)
                    progress_label.place(y=55, x=160)
                    #Create a button to upload articles to the Mongo DB database.
                    DataButton = Button(labelFrame7, text="Upload to Mongo DB-database",  font=("TkHeadingFont", 12), command=lambda: Upload_articles(), width=26)
                    DataButton.place(y=85, x=76)
                    #Calculate the progress per article
                    numOfarticle = len(Article_list)
                    progess = 100/numOfarticle
                    #Iterate over the articles and scrape their content
                    for articles in dicts.keys():
                        url = "https://www.nature.com{0}".format(dicts[articles])
                        response = requests.get(url)
                        #Check if the web page was successfully accessed
                        if response.status_code == 200:
                            print("Successfully opened the web page \n")
                            #accessing the hmtl of the the website
                            soup = BeautifulSoup(response.text, 'html.parser')
                            abstracts = soup.find(
                                'div', class_='c-article-section__content', id='Abs1-content')
                            abstractMag = soup.find(
                                'div', class_="c-article-body main-content")
                            titles = soup.find(
                                'h1', class_='c-article-magazine-title')
                            texts = soup.find('h1', class_="c-article-title")
                            #Check if the article is a magazine article
                            if abstracts == None:
                                print("This ", articles, " is a magazine articles")
                                # Check if necessary elements for a magazine article are present
                                if titles != None and abstractMag != None or texts != None and abstractMag != None:
                                    # Set the item type to indicate it's a magazine article
                                    article_dicts["itemType"] = "magazineArticle"
                                    # Encode and decode the article title to handle special characters
                                    articles = articles.encode("ascii", 'ignore')
                                    articles = articles.decode()
                                    article_dicts["title"] = articles
                                    # Find the publication year of the magazine article
                                    text = soup.find(
                                        'ul', class_="c-article-identifiers", attrs={"data-test": "article-identifier"})

                                    if text == []:
                                        print("No publication year for: ", articles)
                                        article_dicts["pubYear"] = None
                                    else:
                                        # Extract the publication year from the text
                                        for publication in text.find_all('li'):
                                            publication_year = publication.get_text()
                                        length = len(publication_year.split())
                                        publication_year = publication_year.split(" ")[
                                            length-1]
                                        # Check if the extracted publication year is numeric
                                        if publication_year.isnumeric():
                                            article_dicts["pubYear"] = publication_year
                                        else:
                                            print(
                                                "No publication year for: ", articles)
                                            article_dicts["pubYear"] = None
                                    # Find and process the author names of the magazine article
                                    text = soup.find_all(
                                        'a', attrs={'data-test': 'author-name'})
                                    if text == []:  # if:  there no author for the article, print nothing
                                        print("No Authors names for: ", articles)
                                        article_dicts["author"] = None
                                    else:  # else: prints the article's articles_texts
                                        articles_texts = ''
                                        keylist = []
                                        for names in text:
                                            author_text = names.get_text()
                                            # Handle encoding, replacing characters, and formatting author names
                                            author_text = author_text.encode(
                                                "ascii", 'ignore')
                                            author_text = author_text.decode()
                                            author_text = author_text.replace(
                                                '\n', '')
                                            author_text = author_text.replace(
                                                ' ', '')
                                            keylist.append(author_text)
                                        articles_texts = articles_texts + \
                                            " ,".join(keylist)
                                        article_dicts["author"] = articles_texts
                                    # Extract the publication title
                                    texts = soup.find(
                                        "p", class_="c-meta u-ma-0 u-flex-shrink")
                                    if texts == None:
                                        print("No Publication for: ", articles)
                                        article_dicts["pubTitle"] = None
                                    else:
                                        # Process and format the publication title
                                        keylist = []
                                        pub_text = ""
                                        for publics in texts.find('span'):
                                            public_text = publics.get_text()
                                            keylist.append(public_text)
                                        pub_text = pub_text + "".join(keylist)
                                        pub_text = pub_text.replace(' ', '')
                                        pub_text = pub_text.replace('\n', '')
                                        article_dicts["pubTitle"] = pub_text
                                    # Extract the ISSN (International Standard Serial Number)
                                    texts = soup.find(
                                        "p", class_="c-meta u-ma-0 u-flex-shrink")
                                    if texts == []:
                                        print("No ISSN for: ", articles)
                                        article_dicts["issn"] = None
                                    else:
                                        # Process and format the ISSN
                                        keylist = []
                                        issn_text = ''
                                        for ISSN in texts.find_all('span', itemprop='onlineIssn'):
                                            ISSN_text = ISSN.get_text()
                                            keylist.append(ISSN_text)
                                        issn_text = issn_text + "".join(keylist)
                                        issn_text = issn_text.replace(' ', '')
                                        issn_text = issn_text.replace('\n', '')
                                        article_dicts["issn"] = issn_text
                                    # Extract the DOI (Digital Object Identifier)
                                    texts = soup.find(
                                        'article', class_='article-item article-item--open')
                                    if texts == None:
                                        print("No DOI for: ", articles)
                                        article_dicts["doi"] = None
                                    elif texts.find('em') == None:
                                        article_dicts["doi"] = None
                                    else:
                                        # Process the DOI
                                        for DOI in texts.find('em'):
                                            DOI_text = DOI.get_text()
                                        article_dicts["doi"] = DOI_text
                                    article_dicts["url"] = url
                                    keylist = []
                                    ABS_text = ""
                                    if abstractMag == None:
                                        print("No Abstract for: ", articles)
                                        article_dicts["abstract"] = None
                                    else:
                                        for abs in abstractMag.find_all('p'):
                                            ABS = abs.get_text()
                                            keylist.append(ABS)
                                        ABS_text = ABS_text + " ".join(keylist)
                                        ABS_text = ABS_text.encode(
                                            "ascii", 'ignore')
                                        ABS_text = ABS_text.decode()
                                        ABS_text = ABS_text.replace('\n', ' ')
                                        article_dicts["abstract"] = ABS_text
                                    texts = soup.find_all(
                                        'li', class_="c-article-identifiers__item")
                                    if texts == None:
                                        print("NO Date for: ", articles)
                                        article_dicts['date'] = None
                                    else:
                                        for Date in texts:
                                            date_text = Date.get_text()
                                        article_dicts['date'] = date_text
                                    article_dicts['issue'] = None
                                    # Extract the abstract
                                    # Process and format the abstract text
                                    # Extract the article's date
                                    # Extract the article's issue information
                                    texts = soup.find(
                                        'articles', class_='article-item article-item--open')
                                    if texts == None:
                                        print('No Volume for: ', articles)
                                        article_dicts['volume'] = None
                                    else:
                                        # Process and extract the volume information
                                        for Vol in texts:
                                            vol_text = Vol.get_text()  
                                        article_dicts['volume'] = vol_text
                                    # Additional metadata for the article    
                                    article_dicts["libCatalog"] = "Nature"
                                    article_dicts["manualTags"] = None
                                    article_dicts["autoTags"] = None
                                    # Load existing data from Articles.json and update with the new article information
                                    data = json.load(open('Articles.json'))
                                    if type(data) is dict:
                                        data = [data]
                                    data.append(article_dicts.copy())
                                    # Write the updated data to the Articles.json file
                                    with open('Articles.json', 'w') as outfile:
                                        json.dump(data, outfile, indent=0)
                            # If the previous condition was not met (not a journal article) handle appropriately            
                            else:
                                texts = soup.find_all(
                                    'h1', class_="c-article-title")
                                articles_dicts["itemType"] = "journalArticle"# Set the item type as "journalArticle"
                                # getting the Publication Year
                                texts = soup.find(
                                    'ul', class_='c-article-identifiers')
                                if texts == []:  # if:  there no publication year for the article, print nothing
                                    print("No Publication Year for: ", articles)
                                    articles_dicts["pubYear"] = None
                                else:  # else: prints the article's Publication year
                                    for publication in texts.find('time'):
                                        publication_year = publication.get_text()
                                    length = len(publication_year.split())
                                    publication_year = publication_year.split(" ")[
                                        length-1]
                                    if publication_year.isnumeric():
                                        articles_dicts["pubYear"] = publication_year
                                    else:
                                        print("No Publication Year for: ", articles)
                                        articles_dicts["pubYear"] = None
                                    # getting all the author for the article
                                texts = soup.find_all(
                                    'a', attrs={'data-test': 'author-name'})
                                if texts == []:  # if:  there no author for the article, print nothing
                                    print("No Authors names for: ", articles)
                                else: # else: prints the article's articles_texts
                                    articles_texts = ''
                                    keylist = []
                                    for names in texts:
                                        author_text = names.get_text()
                                        author_text = author_text.encode(
                                            "ascii", 'ignore')
                                        author_text = author_text.decode()
                                        keylist.append(author_text)
                                    articles_texts = articles_texts + \
                                        " ,".join(keylist)
                                    articles_dicts["author"] = articles_texts
                                # getting the article title infomation
                                texts = soup.find_all(
                                    'h1', class_="c-article-title")
                                for title in texts:
                                    title_text = title.get_text()
                                    title_text = title_text.encode(
                                        "ascii", 'ignore')
                                    title_text = title_text.decode()
                                articles_dicts["title"] = title_text
                            # getting the article publication info
                                texts = soup.find(
                                    'i', attrs={'data-test': "journal-title"})
                                if texts == []:  # if:  there no publication for the article print nothing
                                    print("No Publication for: ", articles)
                                else: # else: prints the article's Publication info
                                    for public in texts:
                                        publications = public.get_text()
                                    articles_dicts["pubTitle"] = publications
                                texts = soup.find_all(
                                    "span", itemprop="onlineIssn")
                                if texts == []:
                                    print("No ISSN for: ", articles)
                                    articles_dicts["issn"] = None
                                else:
                                    for ISSN in texts:
                                        issn_text = ISSN.get_text()
                                    articles_dicts["issn"] = issn_text
                                # getting the DOI information from the article
                                texts = soup.find(
                                    'li', class_='c-bibliographic-information__list-item c-bibliographic-information__list-item--doi')
                                if texts == []:  # if:  there no DOI for the article, print nothing
                                    print("No DOI for: ", articles)
                                else:  # else: print the article's DOI
                                    for DOI in texts.find("span", class_='c-bibliographic-information__value'):
                                        DOI_text = DOI.get_text()
                                    articles_dicts["doi"] = DOI_text
                                articles_dicts["url"] = url
                                # getting the abtract infomatiom
                                texts = soup.find_all(
                                    'div', class_='c-article-section__content', id='Abs1-content')
                                # else:prints the article's abstract
                                articles_texts = ''
                                # Loop through articles in the retrieved page
                                for abstract in texts:
                                    # Extract and process abstract text
                                    abstract_text = abstract.get_text()
                                    abstract_text = abstract_text.replace(
                                        '\n', " ")
                                    articles_texts = articles_texts + abstract_text + " "
                                    articles_texts = articles_texts.encode(
                                        "ascii", 'ignore')
                                    articles_texts = articles_texts.decode()
                                # Store the abstract in the articles dictionary
                                articles_dicts["abstract"] = articles_texts
                                # Extract publication date
                                texts = soup.find(
                                    'a', attrs={'data-track-action': "publication date"})
                                if texts == []:
                                    print("No Data for: ", articles)
                                    articles_dicts["date"] = None
                                else:
                                    for Date in texts.find("time"):
                                        date_text = Date.get_text()
                                    articles_dicts["date"] = date_text
                                articles_dicts["issue"] = None
                                # Initialize or update volume information for the article
                                texts = soup.find(
                                    'b', attrs={'data-test': "journal-volume"})
                                if texts == None:
                                    print("No Volume number for: ", articles)
                                    articles_dicts["volume"] = None
                                else:
                                    for Vol in texts:
                                        vol_text = Vol.get_text()
                                    vol_text = vol_text.encode("ascii", 'ignore')
                                    vol_text = vol_text.decode()
                                    articles_dicts["volume"] = vol_text
                                # Additional metadata for the article
                                articles_dicts["libCatalog"] = "Nature" # Library catalog information
                                articles_dicts["manualTags"] = None # Manual tags associated with the article
                                articles_dicts["autoTags"] = None # Automatically generated tags associated with the article
                                # Load existing data from Articles.json and update with the new article information
                                data = json.load(open('Articles.json'))
                                if type(data) is dict:
                                    data = [data]
                                data.append(articles_dicts.copy())
                                # Write the updated data to the Articles.json file
                                with open('Articles.json', 'w') as outfile:
                                    json.dump(data, outfile, indent=0)
                            # Update the progress bar and label
                            articles_progress["value"] += progess
                            self.update_idletasks()
                            progress_label.config(
                                text=math.trunc(articles_progress["value"]))
        # Function for searching articles on PubMed
        def article_search_PUBMED():
            # Create a labeled frame for PubMed search
            labelFrame5 = ttk.LabelFrame(
            self.tab3, text="Search Term for PubMed:", width=400, height=190)
            labelFrame5.place(y=80)
            # Create input fields and buttons for searching articles by term on PubMed
            search_term = Label(
                labelFrame5, text='Input term:', font=("TkHeadingFont", 12))
            search_term.place(y=25)
            Term_searchbox = Entry(labelFrame5, font=(
                "TkHeadingFont", 12), width=27)
            Term_searchbox.place(y=25, x=90)
            search_pages = Button(labelFrame5, text="Enter", command=lambda:  page_num(
            ), font=("TkHeadingFont", 10), width=5)
            search_pages.place(y=22, x=345)

            # Function to handle page number selection for PubMed web scraping
            def page_num():
                # Create buttons for generating and scraping articles based on user input
                Gen_articles = Button(labelFrame5, text="Generate articles", command=lambda:  threading.Thread(
                    target=generate_articles_PUBMED).start(), font=("TkHeadingFont", 12), width=14)
                Gen_articles.place(y=135)
                Webscrape_byterm = Button(labelFrame5, text="Scrape by term", command=lambda: threading.Thread(
                    target=ScrapeArticle_bytermPUBMED).start(), font=("TkHeadingFont", 12), width=14)
                Webscrape_byterm.place(x=260, y=135)
                term = Term_searchbox.get()
                url = "https://pubmed.ncbi.nlm.nih.gov/?term={}&page=1".format(term)
                response = requests.get(url)
                if response.status_code == 200:
                    print("Successfully opened the web page \n")
                    pages = 20
                # Create a slider for selecting the number of pages to scrape
                page_Scaler = Scale(labelFrame5, from_=0,to=pages, orient=HORIZONTAL, length=285)
                page_Scaler.place(y=75, x=100)
                Pages = Label(labelFrame5, text='# of pages:',
                              font=("TkHeadingFont", 12))
                Pages.place(y=90)
                
                # Function to generate articles based on PubMed search
                def generate_articles_PUBMED():
                    dicts = {} # Dictionary to store articles and their links
                    Article_list = [] # List to store article titles
                    term = Term_searchbox.get() # Get the search term from the user
                    for numbers in range(0, page_Scaler.get()+1):
                        # Construct the URL for the PubMed search
                        url = "https://pubmed.ncbi.nlm.nih.gov/?term={}&page={}".format(
                            term, numbers)
                        response = requests.get(url) # Send a request to the URL
                        if response.status_code == 200:
                            print("Successfully opened the web page \n")
                            soup = BeautifulSoup(response.text, 'html.parser')
                            texts = soup.find_all('a', class_="docsum-title")# Find article titles
                            for articles in texts:
                                articles_text = articles.get_text()
                                articles_text = articles_text.replace("\n", "")
                                articles_text = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', articles_text, flags=re.M)
                                articles_links = articles.get('href')
                                dicts[articles_text] = articles_links # Store articles and their links in the dictionary
                    # Extract article titles and update the UI            
                    for key in dicts.keys():
                        Article_list.append(key)
                    update(Article_list)
                    # Create a "View Article" button
                    View_Art = Button(labelFrame6, text="View Article", font=(
                        "TkHeadingFont", 11), command=lambda: view_article(), width=13)
                    View_Art.place(y=0, x=535)

                    #Function to get article input, from the browser, and view it.
                    def view_article():
                        article = Article_input.get()
                        webbrowser.open(
                            "https://pubmed.ncbi.nlm.nih.gov/{0}".format(dicts[article]))
                        
                # Function to define Pubmed scrape by term 
                def ScrapeArticle_bytermPUBMED():
                    dicts = {}
                    Article_list = []
                    articles_dicts = {}
                    term = Term_searchbox.get()
                    for numbers in range(0, page_Scaler.get()+1):
                        url = "https://pubmed.ncbi.nlm.nih.gov/?term={}&page={}".format(
                            term, numbers)
                        response = requests.get(url)
                        if response.status_code == 200:
                            print("Successfully opened the web page \n")
                            soup = BeautifulSoup(response.text, 'html.parser')
                            texts = soup.find_all('a', class_="docsum-title")
                            for articles in texts:
                                articles_text = articles.get_text()
                                articles_text = articles_text.replace("\n", "")
                                articles_text = re.sub(
                                    r'(^[ \t]+|[ \t]+(?=:))', '', articles_text, flags=re.M)
                                articles_links = articles.get('href')
                                dicts[articles_text] = articles_links
                    for key in dicts.keys():
                        Article_list.append(key)
                    labelFrame7 = ttk.LabelFrame(
                        self.tab3, text="Articles scraping progress bar: ", width=400, height=140)
                    labelFrame7.place(y=315)
                    articles_progress = ttk.Progressbar(
                        labelFrame7, orient=HORIZONTAL, length=395, mode='determinate')
                    articles_progress.place(y=30)
                    progress_label = Label(labelFrame7, text="")
                    precent_label = Label(labelFrame7, text="%")
                    precent_label.place(y=55, x=186)
                    progress_label.place(y=55, x=160)
                    DataButton = Button(labelFrame7, text="Upload to Mongo DB-database",  font=(
                        "TkHeadingFont", 12), command=lambda: Upload_articles(), width=26)
                    DataButton.place(y=85, x=76)
                    numOfarticle = len(Article_list)
                    progess = 100/numOfarticle

                    for article in dicts.keys():
                        url = "https://pubmed.ncbi.nlm.nih.gov/{0}".format(
                            dicts[article])
                        response = requests.get(url)
                        if response.status_code == 200:
                            print("Successfully opened the web page \n")
                            # accessing the hmtl of the the website
                            soup = BeautifulSoup(response.text, 'html.parser')
                            abstract = soup.find('div', class_="abstract-content selected")
                            if abstract == None:
                                print("This article does not an abstract:", article)
                            else:
                                articles_dicts["itemType"] = "journalArticle"
                                articles_dicts["title"] = article
                                
                                Pubtitles = soup.find(
                                    'p', class_='literature-footer-text')
                                if Pubtitles == None:
                                    print("No Publication Title for", articles)
                                    articles_dicts['pubTitle'] = ""
                                else:
                                    articles_dicts['pubTitle'] = Pubtitles.get_text(
                                    )
                                authors_PMED = soup.find(
                                    'div', class_="authors-list")
                                if authors_PMED == None:
                                    print("No Author for", articles)
                                    articles_dicts['author'] = ""
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
                                    articles_dicts['author'] = authors_name
                                PUBYear = soup.find('span', class_='cit')
                                if PUBYear == None:
                                    print("No publication year for: ", articles)
                                    articles_dicts["pubYear"] = ""
                                else:
                                    public_year = PUBYear.get_text()
                                    public_year = public_year.split(" ")[0]
                                    articles_dicts["pubYear"] = public_year
                                DOI = soup.find('a', class_='id-link',
                                                attrs={"data-ga-action": 'DOI'})
                                if DOI == None:
                                    print("No DOI for: ", articles)
                                    articles_dicts["doi"] = ""
                                else:
                                    doi_text = DOI.get_text()
                                    doi_text = re.sub(
                                        r'(^[ \t]+|[ \t]+(?=:))', '', doi_text, flags=re.M)
                                    doi_text = doi_text.replace('\n', "")
                                    articles_dicts["doi"] = doi_text
                                articles_dicts["url"] = url
                                abstract = soup.find(
                                    'div', class_="abstract-content selected")
                                if abstract == None:
                                    print("No Abstract for: ", articles)
                                    articles_dicts["abstract"] = ""
                                else:
                                    abs = abstract.get_text()
                                    abs = abs.replace("\n", "")
                                    abs = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', abs, flags=re.M)
                                    articles_dicts["abstract"] = abs

                                date = soup.find('span', class_='cit')
                                if date == None:
                                    print("No Date for: ", articles)
                                    articles_dicts['date'] = ""
                                else:
                                    date_text = date.get_text()
                                    date_text = date_text.split(";")[0]
                                    articles_dicts['date'] = date_text
                                volume = soup.find('span', class_='cit')
                                if volume == None:
                                    print("No Volume for: ", articles)
                                    articles_dicts['volume'] = ""
                                else:
                                    vol_text = volume.get_text()
                                    vol_text = vol_text.split(";")[1]
                                    vol_text = vol_text.split("(")[0]
                                    articles_dicts["volume"] = vol_text
                                articles_dicts["issue"] = ""
                                issn = soup.find('span', class_='cit')
                                if issn == None:
                                    print("No ISSN for: ", articles)
                                    articles_dicts['issn'] = ""
                                else:
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
                                    articles_dicts["issn"] = ISSN_text
                                articles_dicts["libCatalog"] = "PubMed"
                                articles_dicts["manualTags"] = ""
                                articles_dicts["autoTags"] = ""
                                data = json.load(open('Articles.json'))
                                if type(data) is dict:
                                    data = [data]
                                data.append(articles_dicts.copy())
                                with open('Articles.json', 'w') as outfile:
                                    json.dump(data, outfile, indent=0)
                        articles_progress["value"] += progess
                        self.update_idletasks()
                        progress_label.config(
                            text=math.trunc(articles_progress["value"]))
                        
        # Function to search articles on Springer
        def article_search_Springer():
            labelFrame5 = ttk.LabelFrame(
            self.tab3, text="Search Term for Springer:", width=400, height=190)
            labelFrame5.place(y=80) 
            search_term = Label(labelFrame5, text='Input term:', font=("TkHeadingFont", 12))
            search_term.place(y=25)
            Term_searchbox = Entry(labelFrame5, font=("TkHeadingFont", 12), width=27)
            Term_searchbox.place(y=25, x=90)
            search_pages = Button(labelFrame5, text="Enter", command=lambda:  page_num(), font=("TkHeadingFont", 10), width=5)
            search_pages.place(y=22, x=345)

            # Function to handle page number selection for Springer web scraping
            def page_num():
                Gen_articles = Button(labelFrame5, text="Generate articles", command=lambda:  threading.Thread(
                    target=generate_articles_Springer).start(), font=("TkHeadingFont", 12), width=14)
                Gen_articles.place(y=135)
                Webscrape_byterm = Button(labelFrame5, text="Scrape by term", command=lambda: threading.Thread(
                    target=ScrapeArticle_bytermSpringer).start(), font=("TkHeadingFont", 12), width=14)
                Webscrape_byterm.place(x=260, y=135)
                term = Term_searchbox.get()
                url = "https://link.springer.com/search/page/1?query={}&facet-content-type=%22Article%22".format(term)
                response = requests.get(url)
                if response.status_code == 200:
                    print("Successfully opened the web page \n")
                    pages = 20
                # Create a slider for selecting the number of pages to scrape
                page_Scaler = Scale(labelFrame5, from_=0,to=pages, orient=HORIZONTAL, length=285)
                page_Scaler.place(y=75, x=100)
                Pages = Label(labelFrame5, text='# of pages:',font=("TkHeadingFont", 12))
                Pages.place(y=90)

                # Function to generate articles 
                def generate_articles_Springer():
                    dicts = {} # Dictionary to store articles and their links
                    Article_list = []# List to store article titles
                    term = Term_searchbox.get()# Get the search term from the user
                    for numbers in range(0, page_Scaler.get()+1):
                        # Construct the URL 
                        url = "https://link.springer.com/search/page/{}?query={}&facet-content-type=%22Article%22".format(numbers,term)
                        response = requests.get(url)
                        if response.status_code == 200:
                            print("Successfully opened the web page \n")
                            soup = BeautifulSoup(response.text, 'html.parser')
                            texts = soup.find_all('a', class_="title")
                            for articles in texts:
                                articles_text = articles.get_text()
                                articles_links = articles.get('href')
                                dicts[articles_text] = articles_links
                    for key in dicts.keys():
                        Article_list.append(key)
                    update(Article_list)
                    View_Art = Button(labelFrame6, text="View Article", font=(
                        "TkHeadingFont", 11), command=lambda: view_article(), width=13)
                    View_Art.place(y=0, x=535)
                    ####
                    def view_article():
                        article = Article_input.get()
                        webbrowser.open("https://link.springer.com{0}".format(dicts[article]))

                #Function to scrape articles according to term within Springer
                def ScrapeArticle_bytermSpringer():
                    dicts = {}
                    Article_list = []
                    articles_dicts = {}
                    term = Term_searchbox.get()
                    for numbers in range(1, page_Scaler.get()+1):
                        url = "https://link.springer.com/search/page/{}?query={}&facet-content-type=%22Article%22".format(numbers,term)
                        response = requests.get(url)
                        if response.status_code == 200:
                            print("Successfully opened the web page \n")
                            soup = BeautifulSoup(response.text, 'html.parser')
                            texts = soup.find_all('a', class_ = "title")
                            for articles in texts:
                                articles_text = articles.get_text()
                                articles_text = articles_text.replace("\n", "")
                                articles_text = re.sub(
                                    r'(^[ \t]+|[ \t]+(?=:))', '', articles_text, flags=re.M)
                                articles_links = articles.get('href')
                                dicts[articles_text] = articles_links
                    for key in dicts.keys():
                        Article_list.append(key)
                    labelFrame7 = ttk.LabelFrame(
                        self.tab3, text="Articles scraping progress bar: ", width=400, height=140)
                    labelFrame7.place(y=315)
                    articles_progress = ttk.Progressbar(
                        labelFrame7, orient=HORIZONTAL, length=395, mode='determinate')
                    articles_progress.place(y=30)
                    progress_label = Label(labelFrame7, text="")
                    precent_label = Label(labelFrame7, text="%")
                    precent_label.place(y=55, x=186)
                    progress_label.place(y=55, x=160)
                    DataButton = Button(labelFrame7, text="Upload to Mongo DB-database",  font=(
                        "TkHeadingFont", 12), command=lambda: Upload_articles(), width=26)
                    DataButton.place(y=85, x=76)
                    numOfarticle = len(Article_list)
                    progess = 100/numOfarticle
                    for article in dicts.keys():
                        url = "https://link.springer.com{}".format(dicts[article])
                        response = requests.get(url)
                        if response.status_code == 200:
                            print("Successfully opened the web page \n")
                            # accessing the hmtl of the the website
                            soup = BeautifulSoup(response.text, 'html.parser')
                            abstract = soup.find('div', class_="main-content")
                            if abstract == None:
                                print("This article does not an abstract:", article)
                            else:
                                articles_dicts["itemType"] = "journalArticle"
                                article_name = article.encode("ascii", 'ignore')
                                article_name = article_name.decode()
                                articles_dicts["title"] = article_name
                                Pubtitles = soup.find('i', attrs = {'data-test': 'journal-title'})
                                if Pubtitles == None:
                                    print("No Publication Title for", articles)
                                    articles_dicts['pubTitle'] = ""
                                else:
                                    articles_dicts['pubTitle'] = Pubtitles.get_text()
                                authors = soup.find_all('a', attrs = {'data-test' : 'author-name'})
                                if authors == None:
                                    print("No Author for", articles)
                                    articles_dicts['author'] = ""
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
                                    articles_dicts['author'] = authors_name
                                PUBYear = soup.find('span', class_  = 'c-bibliographic-information__value')
                                if PUBYear == None:
                                    print("No publication year for: ", articles)
                                    articles_dicts["pubYear"] = ""
                                else:
                                    public_year = PUBYear.get_text()
                                    public_year = public_year.split(" ")[2]
                                    articles_dicts["pubYear"] = public_year
                                DOI = soup.find('li', class_="c-bibliographic-information__list-item c-bibliographic-information__list-item--doi")
                                if DOI == None:
                                    print("No DOI for: ", articles)
                                    articles_dicts["doi"] = ""
                                else:
                                    for doi in DOI.find('span', class_ = 'c-bibliographic-information__value'):
                                        doi_text = doi.get_text()
                                        doi_text = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', doi_text, flags=re.M)
                                        doi_text = doi_text.replace('\n', "")
                                    articles_dicts["doi"] = doi_text
                                articles_dicts["url"] = url
                                abstract = soup.find('div', class_="main-content")
                                if abstract == None:
                                    print("No Abstract for: ", articles)
                                    articles_dicts["abstract"] = ""
                                else:
                                    for springer_abstract in abstract.find_all('p'):
                                        abs = springer_abstract.get_text()
                                        abs = abs.replace("\n", "")
                                        abs = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', abs, flags=re.M)
                                        abs = abs.encode("ascii", 'ignore')
                                        abs = abs.decode()
                                    articles_dicts["abstract"] = abs
                                date = soup.find('span', class_='c-bibliographic-information__value')
                                if date == None:
                                    print("No Date for: ", articles)
                                    articles_dicts['date'] = ""
                                else:
                                    date_text = date.get_text()
                                    articles_dicts['date'] = date_text
                                volume = soup.find('p', class_='c-bibliographic-information__citation')
                                if volume == None:
                                    print("No Volume for: ", articles)
                                    articles_dicts['volume'] = ""
                                else:
                                    for vol in volume.find('b'):
                                        vol_text = vol.get_text()
                                    articles_dicts["volume"] = vol_text
                                articles_dicts["issue"] = ""
                                articles_dicts['issn'] = ""
                                articles_dicts["libCatalog"] = "Springer"
                                articles_dicts["manualTags"] = ""
                                articles_dicts["autoTags"] = ""
                                data = json.load(open('Articles.json'))
                                if type(data) is dict:
                                    data = [data]
                                data.append(articles_dicts.copy())
                                with open('Articles.json', 'w') as outfile:
                                    json.dump(data, outfile, indent=0)
                        articles_progress["value"] += progess
                        self.update_idletasks()
                        progress_label.config(
                            text=math.trunc(articles_progress["value"]))

#Function to upload articles to the .json file
def Upload_articles():
    with open("Articles.json") as file:
        fileData = json.load(file)
    for singleJson in fileData:
        scraper_doi = singleJson["doi"]
        result = collection.find_one({"doi": scraper_doi})
        if (result == None):
            collection.insert_one(singleJson)
    os.remove("Articles.json")


if __name__ == '__main__':
    root = Root()


root.mainloop()

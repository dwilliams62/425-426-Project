import tkinter as tk
from tkinter import filedialog
from tkinter import Scale
from tkinter import ttk

# import functions from files that we define
from fileFunctions import process_rdf_file, download_as_rdf, upload_to_website
from websiteScraping import scrape_pubmed, scrape_springer
from machineLearning import add_category

# global variables that can be used for any function, stores the data we're working with and which website we're scraping
processed_data = None
website_chosen = None
percentage = 0.0

# Create all the buttons and labels shown on starting the application
def create_startup_buttons(root):
    # Create labels
    title_label = tk.Label(root, text="CLIMAT3 Scraper and Classifier", font=("Arial", 16))
    instruction_label = tk.Label(root, text="How would you like to upload the data?", font=("Arial", 12))

    # Create buttons
    upload_button = tk.Button(root, text="Upload my own RDF", command=upload_own_rdf)
    scrape_button = tk.Button(root, text="Scrape from website", command=scrape_website_initialize)
    machine_learning_test_button = tk.Button(root, text="Test Machine Learning", command=machine_learning_test_initialize)

    # Pack the labels and buttons into the main window
    title_label.pack(pady=10)
    instruction_label.pack(pady=5)
    upload_button.pack(pady=10)
    scrape_button.pack(pady=10)
    machine_learning_test_button.pack(pady=10)



# When the user chooses to upload their own RDF, this is where the data will be processed,
# And then the user will be sent to the categorizer
def upload_own_rdf():
    global processed_data #reference the global variable to be able to update it

    #prompts the user to pick a file on their computer to upload that ends in .rdf
    file_path = filedialog.askopenfilename(filetypes=[("RDF Files", "*.rdf")]) 

    #if the user picks an rdf file, processes it and then goes to the categorizer. otherwise does nothing
    if file_path:
        processed_data = process_rdf_file(file_path)
        categorize_data_initialize()



# starts the web scraper section, asks the user to pick a website and how many pages of data to scrape
# then scrapes the data into processed_data before sending the program to the categorizer
def scrape_website_initialize():
    global processed_data #reference the global variable to be able to update it

    #clear out all the current tkinter objects on the page
    for widget in root.winfo_children():
        widget.pack_forget()
    
    # Create label
    website_label = tk.Label(root, text="Select a website to scrape from")
    website_label.pack()

    # Create the buttons to pick what website
    website_frame = tk.Frame(root)
    website_frame.pack()

    pubmed_button = tk.Button(website_frame, text="Pubmed", command=set_website_pubmed)
    pubmed_button.pack(side=tk.LEFT, padx=5)

    springer_button = tk.Button(website_frame, text="Springer", command=set_website_springer)
    springer_button.pack(side=tk.LEFT, padx=5)

    #create a label
    label = tk.Label(root, text="Enter term to search by")
    label.pack(pady=10)

    #create a bar the user can type in a search term to search by
    entry = tk.Entry(root)
    entry.pack()

    # Create another label
    pages_label = tk.Label(root, text="How many pages of articles would you like to scrape?")
    pages_label.pack(pady=10)

    # Adds a scale bar to select number of pages from 1 to 10
    pages_scale = Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, length=200)
    pages_scale.pack()

    # Create the final submit button to start scraping
    scrape_button = tk.Button(root, text="Scrape!", command=lambda: scrape_website_process(pages_scale, entry.get()))
    scrape_button.pack(pady=10)

#if the springer button is pressed, use springer
def set_website_springer():
    global website_chosen
    website_chosen = 'springer'

#if the pubmed button is pressed, use pubmed
def set_website_pubmed():
    global website_chosen
    website_chosen = 'pubmed'

#actually scrapes the websites then sends it to the categorizers
def scrape_website_process(scale_widget, scrape_term):
    #if no website is chosen, button does nothing
    if website_chosen:
        #grabs the value of the scale
        value = scale_widget.get()

        #removes all widgets on the gui currently
        for widget in root.winfo_children():
            widget.pack_forget()

        #add a label
        pages_label = tk.Label(root, text="Opening....")
        pages_label.pack()

        # Create a progress bar
        progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        progress.pack(padx=20, pady=5)

        root.update()

        global processed_data #reference global variable to change it
        global percentage 


        #depending on the website chosen, call correct scraping function
        if website_chosen == 'pubmed':
            processed_data, percentage = scrape_pubmed(progress, value, scrape_term, pages_label, root)
        if website_chosen == 'springer':
            processed_data, percentage = scrape_springer(progress, value, scrape_term, pages_label, root)
        
        #temporary measure, prints the data that was passed by web scraper
        for dictionary in processed_data:
            print("\nDictionary:")
            for key, value in dictionary.items():
                print(f"Key: {key}, Value: {value}")

        #start the categorizing of the data
        categorize_data_initialize()
        


#a function to initialize preset data into the processed data for testing purposes
def machine_learning_test_initialize():
    global processed_data
    processed_data = [
        {"key1": "value1", "key2": "value2"},
        {"key3": "value3", "key4": "value4"},
        {"key5": "value5", "key6": "value6"}
    ]
    categorize_data_initialize()

#at this point data will have been uploaded somehow, and the program will then use the machine learning algorithm to
#to classify each article given into the correct category
def categorize_data_initialize():
    #remove all widgets currently inside
    for widget in root.winfo_children():
        widget.pack_forget()

    #add a label to show what's happening
    pages_label = tk.Label(root, text="Categorizing....")
    pages_label.pack()
    
    # Create a progress bar
    progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
    progress.pack(padx=20, pady=5)

    root.update()

    global processed_data #reference global variable to change it

    #using the current data, add the correct category to each article in processed_data
    processed_data = add_category(progress, processed_data, root)

    #send the user to the final screen
    use_data_initialize()



#from here the user will decide to download the data as an rdf or upload it to the website
def use_data_initialize():
    for widget in root.winfo_children():
        widget.pack_forget()

    # define label
    label = tk.Label(root, text="What would you like to do with the data?")
    label.pack(pady=10)

    label2 = tk.Label(root, text="(The percentage of data that is missing is {:.2f}%)".format(percentage))
    label2.pack(pady=10)

    # Button - Upload to website
    upload_button = tk.Button(root, text="Upload to website", command=lambda: [upload_to_website(processed_data),show_results_initialize()])
    upload_button.pack(pady=5)

    # Button - Download as Zotero RDF file
    download_button = tk.Button(root, text="Download as Zotero RDF file", command=lambda: download_as_rdf(processed_data))
    download_button.pack(pady=5)

    scrape_again_button = tk.Button(root, text="Discard and Scrape again", command=scrape_again_initialize)
    scrape_again_button.pack(pady=5)

def exit_gui(): 
    root.destroy()

def scrape_again_initialize():
    for widget in root.winfo_children():
        widget.pack_forget()
   
    global processed_data
    processed_data = None
    create_startup_buttons(root)

def show_results_initialize(): 
    for widget in root.winfo_children():
        widget.pack_forget()
    
    #label to show succesful processing of data
    label = tk.Label(root, text="Congrats you have successfully Uploaded the data!")
    label.pack(pady=15)

    exit_button = tk.Button(root, text= "Exit",command = exit_gui)
    exit_button.pack(pady=5)

    scrape_again_button = tk.Button(root, text="Back to Title", command=scrape_again_initialize)
    scrape_again_button.pack(pady=5)






# Create the main window
root = tk.Tk()
root.title("CLIMAT3 Scraper and Classifier")

create_startup_buttons(root)
# Run the Tkinter event loop
root.mainloop()
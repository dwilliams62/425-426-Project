import tkinter as tk
from tkinter import filedialog
from tkinter import Scale
from tkinter import ttk

# import functions from files that we define
from fileFunctions import process_file, download_data, upload_to_website
from websiteScraping import scrape_pubmed, scrape_springer
from machineLearning import add_category

# global variables that can be used for any function, stores the data we're working with and which website we're scraping
processed_data = None
website_chosen = None
percentage = 0.0
error = None


    
# Create all the buttons and labels shown on starting the application
def create_startup_buttons(root):
    # Create labels
    title_label = tk.Label(root, text="CLIMAT3 Scraper and Classifier", font=("Arial", 16),width=40,bg="green",fg="white")
    space_label = tk.Label(root, text="", height=3)
    
    instruction_label = tk.Label(root, text="How would you like to upload the data?", font=("Arial", 12),fg= "green")
    space_label2 = tk.Label(root, text="", height=5)

    # Create buttons
    upload_button = tk.Button(root, text="Upload my own data", command=upload_own_data, width=20,bg='#347aeb',fg="white")
    scrape_button = tk.Button(root, text="Scrape from website", command=scrape_website_initialize,width =20,bg='#347aeb',fg="white")

    # Pack the labels and buttons into the main window
    title_label.pack(pady=(100,10))
    space_label.pack()
    instruction_label.pack(pady=5)
    space_label2.pack()
    upload_button.pack(pady=10)
    scrape_button.pack(pady=10)



# When the user chooses to upload their own RDF, this is where the data will be processed,
# And then the user will be sent to the categorizer
def upload_own_data():
    global processed_data #reference the global variable to be able to update it

    #prompts the user to pick a file on their computer to upload that ends in .rdf
    file_path = filedialog.askopenfilename() 

    #if the user picks an rdf file, processes it and then goes to the categorizer. otherwise does nothing
    if file_path:
        processed_data = process_file(file_path)
        categorize_data_initialize()



# starts the web scraper section, asks the user to pick a website and how many pages of data to scrape
# then scrapes the data into processed_data before sending the program to the categorizer
def scrape_website_initialize():
    global processed_data #reference the global variable to be able to update it

    #clear out all the current tkinter objects on the page
    for widget in root.winfo_children():
        widget.pack_forget()
    
    # Create label
    website_label = tk.Label(root, text="Select a website to scrape from",font=("Verdana",14),fg='#1a54b0')
    website_label.pack()

    # Create the buttons to pick what website
    website_frame = tk.Frame(root,width= 200,height=250)
    website_frame.pack()

    pubmed_button = tk.Button(website_frame, text="Pubmed",bg="white",fg='#347aeb' ,command=set_website_pubmed)
    pubmed_button.pack(side=tk.LEFT, padx=5)

    springer_button = tk.Button(website_frame, text="Springer",bg="white",fg="red", command=set_website_springer)
    springer_button.pack(side=tk.LEFT, padx=5)

    space_label = tk.Label(root, text="", height=3)
    space_label.pack()

    #create a border frame
    border_frame = tk.Frame(root, borderwidth=2, relief="ridge",bg='#347aeb')
    border_frame.pack(padx=5, pady=5)

    #create a label
    label = tk.Label(border_frame, text="Enter term to search by",padx=10,pady=10,bg="white",font=('Verdana',10))
    label.pack()

    #create a bar the user can type in a search term to search by
    entry = tk.Entry(root,width=20)
    entry.pack()

    space_label2 = tk.Label(root, text="", height=2)
    space_label2.pack()

    # Create another label
    pages_label = tk.Label(root, text="How many pages of articles would you like to scrape?",font=('Verdana',10))
    pages_label.pack(pady=10)

    pages_frame = tk.Frame(root)
    pages_frame.pack()

    #page range stuff
    start_page = tk.Label(pages_frame, text="Select Your Page range ")
    start_page.pack(side=tk.LEFT, pady=5)

    start_entry =tk.Entry(pages_frame, width=5)
    start_entry.pack(side=tk.LEFT, pady=5)

    end_entry = tk.Entry(pages_frame, width=5)
    end_entry.pack(side=tk.LEFT, pady=5)

    #add default entries
    start_entry.insert(0, "1")  # "0" is the default value for start_entry
    end_entry.insert(0, "5")   # "10" is the default value for end_entry

    space_label3 = tk.Label(root, text="", height=2)
    space_label3.pack()

    # Create the final submit button to start scraping
    scrape_button = tk.Button(root, text="Scrape!",bg='#347aeb',fg="white",font=("Arial",14) ,command=lambda: scrape_website_process(start_entry.get(), end_entry.get(), entry.get()))
    scrape_button.pack(pady=10)

    scrape_again_button = tk.Button(root, text="Back", command=scrape_again_initialize,bg="white",fg="green",font=("Verdana",8))
    scrape_again_button.pack(pady=20)

#if the springer button is pressed, use springer
def set_website_springer():
    global website_chosen
    website_chosen = 'springer'

#if the pubmed button is pressed, use pubmed
def set_website_pubmed():
    global website_chosen
    website_chosen = 'pubmed'

#actually scrapes the websites then sends it to the categorizers
def scrape_website_process(start,end, scrape_term):
    #if no website is chosen, button does nothing
    if website_chosen:
        #removes all widgets on the gui currently
        for widget in root.winfo_children():
            widget.pack_forget()

        #add a label
        pages_label = tk.Label(root, text="Opening....",font=("Verdana",12),fg="green")
        pages_label.pack()

        # Create a progress bar
        progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        progress.pack(padx=20, pady=5)

        root.update()

        global processed_data #reference global variable to change it
        global percentage 
        global error


        #depending on the website chosen, call correct scraping function
        if website_chosen == 'pubmed':
            processed_data, percentage, error = scrape_pubmed(progress, start,end,scrape_term, pages_label, root)
        if website_chosen == 'springer':
            processed_data, percentage, error = scrape_springer(progress, start, end,scrape_term, pages_label, root)
        print(error)
        #temporary measure, prints the data that was passed by web scraper
        if error:
            show_err() 

        else:
            for dictionary in processed_data:
                print("\nDictionary:")
                for key, value in dictionary.items():
                    print(f"Key: {key}, Value: {value}")

            #start the categorizing of the data
            categorize_data_initialize()
        
#a function to show and error if the user entered the wrong page range :
def show_err():
    #remove all widgets currently inside
    for widget in root.winfo_children():
        widget.pack_forget()
    
    label = tk.Label(text="You entered the wrong range for the page Number")
    label.pack(pady=10)

    scrape_again_button = tk.Button(root, text="Back to Title", command=scrape_again_initialize)
    scrape_again_button.pack(pady=5)
    


#at this point data will have been uploaded somehow, and the program will then use the machine learning algorithm to
#to classify each article given into the correct category
def categorize_data_initialize():
    #remove all widgets currently inside
    for widget in root.winfo_children():
        widget.pack_forget()

    #add a label to show what's happening
    pages_label = tk.Label(root, text="Categorizing....",font=("Verdana",12),fg="green")
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

    global website_chosen
    if (website_chosen):
        # Button - Upload to website
        upload_button = tk.Button(root, text="Upload to website", command=lambda: [upload_to_website(processed_data),show_results_initialize()])
        upload_button.pack(pady=5)
    else:
        # Button - Download as Zotero RDF file
        download_button = tk.Button(root, text="Download as CSL JSON file", command=download_data_initialize)
        download_button.pack(pady=5)

    scrape_again_button = tk.Button(root, text="Discard and Scrape again", command=scrape_again_initialize)
    scrape_again_button.pack(pady=5)

def download_data_initialize():
    for widget in root.winfo_children():
        widget.pack_forget()

    #create a label
    label = tk.Label(root, text="Enter directory path")
    label.pack(pady=10)

    #create a bar the user can type in a search term to search by
    entry = tk.Entry(root)
    entry.pack()

    #create a label
    label1 = tk.Label(root, text="Enter filename")
    label1.pack(pady=10)

    #create a bar the user can type in a search term to search by
    entry1 = tk.Entry(root)
    entry1.pack()

    download_button = tk.Button(root, text="Download", 
                                    command=lambda: [download_data(processed_data, entry.get(), entry1.get()),show_results_initialize()])
    download_button.pack(pady=5)

def exit_gui(): 
    root.destroy()

def scrape_again_initialize():
    for widget in root.winfo_children():
        widget.pack_forget()
   
    global processed_data
    global website_chosen
    global percentage
    processed_data = None
    website_chosen = None
    percentage = 0.0
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

#resize(root)
root.geometry("800x600")
create_startup_buttons(root)
# Run the Tkinter event loop
root.mainloop()
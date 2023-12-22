import tkinter as tk
from tkinter import filedialog
from tkinter import Scale
from tkinter import ttk
from fileFunctions import process_rdf_file, download_as_rdf, upload_to_website
from websiteScraping import scrape_pubmed, scrape_springer
from machineLearning import add_category

processed_data = None
website_chosen = None

# Create all the buttons and labels shown on starting the application
def create_startup_buttons(root):
    # Create labels
    title_label = tk.Label(root, text="CLIMAT3 Scraper and Classifier", font=("Arial", 16))
    instruction_label = tk.Label(root, text="How would you like to upload the data?", font=("Arial", 12))

    # Create buttons
    upload_button = tk.Button(root, text="Upload my own RDF", command=upload_own_rdf)
    scrape_button = tk.Button(root, text="Scrape from website", command=scrape_website_initialize)

    # Pack the labels and buttons into the main window
    title_label.pack(pady=10)
    instruction_label.pack(pady=5)
    upload_button.pack(pady=10)
    scrape_button.pack(pady=10)



# When the user chooses to upload their own RDF, this is where the data will be processed,
# And then the user will be sent to the classifier
def upload_own_rdf():
    global processed_data

    file_path = filedialog.askopenfilename(filetypes=[("RDF Files", "*.rdf")])

    if file_path:
        processed_data = process_rdf_file(file_path)  # Assuming file_path is known or obtained from user input

        categorize_data_initialize()



def scrape_website_initialize():
    global processed_data

    for widget in root.winfo_children():
        widget.pack_forget()
    
    # Label - Select a website to scrape from
    website_label = tk.Label(root, text="Select a website to scrape from")
    website_label.pack()

    # Buttons for website selection (Pubmed and Springer)
    website_frame = tk.Frame(root)
    website_frame.pack()

    pubmed_button = tk.Button(website_frame, text="Pubmed", command=set_website_pubmed)
    pubmed_button.pack(side=tk.LEFT, padx=5)

    springer_button = tk.Button(website_frame, text="Springer", command=set_website_springer)
    springer_button.pack(side=tk.LEFT, padx=5)

    # Label - How many pages of articles would you like to scrape?
    pages_label = tk.Label(root, text="How many pages of articles would you like to scrape?")
    pages_label.pack()

    # Scale widget for selecting the number of pages
    pages_scale = Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, length=200)
    pages_scale.pack()

    # Button to initiate scraping
    scrape_button = tk.Button(root, text="Scrape!", command=lambda: scrape_website_process(pages_scale))
    scrape_button.pack(pady=10)

def set_website_springer():
    global website_chosen
    website_chosen = 'springer'

def set_website_pubmed():
    global website_chosen
    website_chosen = 'pubmed'

def scrape_website_process(scale_widget):
    if website_chosen:
        value = scale_widget.get()

        for widget in root.winfo_children():
            widget.pack_forget()

        # Create a progress bar
        progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        progress.pack(padx=20, pady=20)

        global processed_data

        if website_chosen == 'pubmed':
            processed_data = scrape_pubmed(progress, value)
        if website_chosen == 'springer':
            processed_data = scrape_springer(progress, value)
        
        categorize_data_initialize()
        



def categorize_data_initialize():
    # Update the label text to indicate processing is complete
    for widget in root.winfo_children():
        widget.pack_forget()

    # Create a progress bar
    progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
    progress.pack(padx=20, pady=20)

    global processed_data

    processed_data = add_category(progress, processed_data)
    use_data_initialize()

def use_data_initialize():
    for widget in root.winfo_children():
        widget.pack_forget()

    # Label - What would you like to do with the data?
    label = tk.Label(root, text="What would you like to do with the data?")
    label.pack(pady=10)

    # Button - Upload to website
    upload_button = tk.Button(root, text="Upload to website", command=lambda: upload_to_website(processed_data))
    upload_button.pack(pady=5)

    # Button - Download as Zotero RDF file
    download_button = tk.Button(root, text="Download as Zotero RDF file", command=lambda: download_as_rdf(processed_data))
    download_button.pack(pady=5)

# Create the main window
root = tk.Tk()
root.title("CLIMAT3 Scraper and Classifier")

create_startup_buttons(root)

# Run the Tkinter event loop
root.mainloop()
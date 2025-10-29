import pandas as pd #Import pandas to read and process the CSV file.
import random #Import random to select a joke randomly from the list.
from tkinter import * #Import all components from Tkinter for GUI creation.

JOKES = [] #Global list to store (setup, punchline) tuples.
CURRENT_PUNCHLINE = "" #Global variable to store the punchline of the current joke.
STATE = "SETUP" #Global state: Tracks if the next action should reveal the punchline.
CSV_FILE = 'shortjokes.csv' #Defines the name of the new dataset file.

def load_and_prepare_jokes(file_path): #Function to load and parse jokes from the CSV.
    try: #Begin exception handling block.
        df = pd.read_csv(file_path) #Read the CSV file into a DataFrame.
        #Filter the DataFrame: selects rows where the 'Joke' column contains a '?'.
        df_filtered = df[df['Joke'].str.contains(r'\?', na=False)] 
        
        #Return a list of (setup, punchline) tuples using a list comprehension.
        return [(joke.split('?', 1)[0].strip(), joke.split('?', 1)[1].strip().replace('\n', ' ')) 
                for joke in df_filtered['Joke']] #Split each joke on the first '?'.
    except: #Catch any errors (e.g., file not found, wrong column name).
        return [] #Return an empty list if loading fails.

def tellJoke(): #Function to select and display a new joke's setup.
    global CURRENT_PUNCHLINE, STATE #Declare global variables for modification.
    
    if not JOKES: #Check if the joke list is empty.
        joke_label.config(text="No jokes loaded.") #Display error message in the GUI.
        return #Exit the function if no jokes are available.

    setup, punchline = random.choice(JOKES) #Select a random joke (setup and punchline).
    CURRENT_PUNCHLINE = punchline #Store the punchline globally.
    STATE = "PUNCHLINE" #Change state to indicate punchline is ready to be shown.
    
    joke_label.config(text=f"Setup: {setup}?") #Update the label to display the joke setup.
    tell_button.config(state=DISABLED) #Disable the "Tell me a Joke" button.
    punchline_button.config(state=NORMAL) #Enable the "Show Punchline" button.

def showPunchline(): #Function to reveal the punchline and reset the state.
    global STATE #Declare global state variable.

    if STATE != "PUNCHLINE": return #Prevent execution if the state is incorrect.

    #Append the punchline to the existing setup text in the label.
    joke_label.config(text=f"{joke_label.cget('text')} \n\nPunchline: {CURRENT_PUNCHLINE}")
    
    punchline_button.config(state=DISABLED) #Disable the "Show Punchline" button.
    tell_button.config(state=NORMAL) #Enable the "Tell me a Joke" button.
    STATE = "SETUP" #Reset state to allow a new joke request.

root = Tk() #Create the main Tkinter window (root object).
root.title("Jokes When Sad") #Set the title of the window.

JOKES = load_and_prepare_jokes(CSV_FILE) #Load the jokes dataset on program startup.

joke_label = Label(root, text="Say 'Alexa tell me a Joke' or press the button below.", #Create label for joke text/instructions.
                   font=("Arial", 12), wraplength=400, justify=LEFT) #Set font, wrap length, and left justification.
joke_label.pack(padx=20, pady=20) #Place the label in the window with padding.

tell_button = Button(root, text="Alexa tell me a Joke", command=tellJoke, #Create the "Tell Joke" button.
                     font=("Arial", 14, "bold")) #Set the button's font.
tell_button.pack(fill='x', padx=20, pady=5) #Place the button and stretch it horizontally.

punchline_button = Button(root, text="Show Punchline", command=showPunchline, #Create the "Show Punchline" button.
                          font=("Arial", 14), state=DISABLED) #Set font and disable it initially.
punchline_button.pack(fill='x', padx=20, pady=5) #Place the button and stretch it horizontally.

Button(root, text="Quit", command=root.quit).pack(fill='x', padx=20, pady=5) #Create and place the 'Quit' button.

root.mainloop()
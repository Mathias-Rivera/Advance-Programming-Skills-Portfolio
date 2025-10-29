import random #Import the random module for generating numbers and operations
from tkinter import * #Import everything from the tkinter library for GUI development

# \\\ Global Game State Variables \\\
SCORE = 0 #Initialize the user's score
QUESTION_COUNT = 0 #Initialize the question counter
MAX_QUESTIONS = 10 #Define the total number of questions per quiz
DIFFICULTY = 1 #Default difficulty level (1: Easy, 2: Moderate, 3: Advanced)
ATTEMPT_COUNT = 0 #Tracks attempts for the current question
CURRENT_ANSWER = 0 #Stores the correct answer for the current problem
NUMBER_DIGITS = {1: (1, 9), 2: (10, 99), 3: (1000, 9999)} #Map difficulty to min/max range

# \\\ Tkinter Root and UI Elements \\\
root = Tk() #Create the main window
root.title("Arithmetic Quiz") #Set the window title

#Widgets for the main game area (initialized later)
problem_label = None #Label to display the arithmetic problem
answer_entry = None #Entry field for the user's answer
feedback_label = None #Label to show feedback (Correct/Incorrect)
score_label = None #Label to display the current score
question_label = None #Label to display the question count
menu_frame = None #Frame for the difficulty selection menu
game_frame = None #Frame for the quiz problems
result_frame = None #Frame for the final results

# \\\ Core Logic Functions \\\

def randomInt(level): #For running the random integers
    #Determine the number range based on the difficulty level
    min_val, max_val = NUMBER_DIGITS.get(level, (1, 9))
    #Return a random integer within the determined range
    return random.randint(min_val, max_val)

def decideOperation(): #For running random operation
    #Randomly select a mathematical operation ('+' or '-')
    return random.choice(['+', '-'])

def displayMenu():  #Menu 
    #Hide any active frames to show the menu
    if game_frame: game_frame.pack_forget()
    if result_frame: result_frame.pack_forget()

    global menu_frame #Access the global menu frame variable
    menu_frame = Frame(root, padx=20, pady=20) #Create the menu frame
    menu_frame.pack(padx=10, pady=10) #Display the menu frame

    Label(menu_frame, text="DIFFICULTY LEVEL", font=("Arial", 16, "bold")).pack(pady=10) #Title label

    #Create buttons for each difficulty level, calling setDifficulty with the level number
    Button(menu_frame, text="1. Easy (Single Digit)", command=lambda: setDifficulty(1)).pack(fill='x', pady=5)
    Button(menu_frame, text="2. Moderate (Double Digit)", command=lambda: setDifficulty(2)).pack(fill='x', pady=5)
    Button(menu_frame, text="3. Advanced (4-Digit)", command=lambda: setDifficulty(3)).pack(fill='x', pady=5)
    
def setDifficulty(level): #When user picks a difficulty, this will reset all variables and initiate setupGameUI
    #Set the global difficulty and start the game
    global DIFFICULTY #Access the global difficulty variable
    DIFFICULTY = level #Set the chosen level
    global SCORE, QUESTION_COUNT, ATTEMPT_COUNT #Reset game state variables
    SCORE = 0 #Reset score
    QUESTION_COUNT = 0 #Reset question count
    ATTEMPT_COUNT = 0 #Reset attempt count
    menu_frame.pack_forget() #Hide the menu
    setupGameUI() #Initialize the game interface
    nextProblem() #Start the first question

def setupGameUI(): #
    #Setup the main game interface elements (Submit button is omitted)
    global game_frame, problem_label, answer_entry, feedback_label, score_label, question_label
    
    game_frame = Frame(root, padx=20, pady=20) #Create the game frame
    game_frame.pack(padx=10, pady=10) #Display the game frame

    question_label = Label(game_frame, text="Question 1/10", font=("Arial", 12)) #Question counter label
    question_label.pack(pady=5)

    score_label = Label(game_frame, text=f"Score: {SCORE}", font=("Arial", 12)) #Score label
    score_label.pack(pady=5)

    problem_label = Label(game_frame, text="", font=("Arial", 20)) #Problem display label
    problem_label.pack(pady=10)

    answer_entry = Entry(game_frame, font=("Arial", 16), justify='center') #Input field for answer
    answer_entry.pack(pady=5)
    answer_entry.bind('<Return>', lambda event: checkAnswer()) #Bind Enter key to submission

    feedback_label = Label(game_frame, text="", font=("Arial", 12), fg="red") #Feedback message label
    feedback_label.pack(pady=5)

def nextProblem():
    #Generates and displays the next problem
    global QUESTION_COUNT, ATTEMPT_COUNT, CURRENT_ANSWER
    
    if QUESTION_COUNT >= MAX_QUESTIONS:
        displayResults() #End quiz if max questions reached
        return

    QUESTION_COUNT += 1 #Increment question counter
    ATTEMPT_COUNT = 1 #Reset attempt count to 1 for a new question
    
    #Update UI labels
    question_label.config(text=f"Question {QUESTION_COUNT}/{MAX_QUESTIONS}")
    score_label.config(text=f"Score: {SCORE}")
    feedback_label.config(text="")
    answer_entry.delete(0, END) #Clear previous answer
    answer_entry.focus_set() #Set focus to the entry field for immediate typing

    #Generate the problem components
    num1 = randomInt(DIFFICULTY)
    num2 = randomInt(DIFFICULTY)
    operation = decideOperation()

    #Calculate the correct answer
    if operation == '+':
        CURRENT_ANSWER = num1 + num2
    else:
        CURRENT_ANSWER = num1 - num2 #Calculate subtraction result

    #Construct and display the problem string
    problem_str = f"{num1} {operation} {num2} = ?"
    problem_label.config(text=problem_str)

def checkAnswer():
    #Check the user's submitted answer
    global SCORE, ATTEMPT_COUNT

    try:
        user_answer = int(answer_entry.get()) #Get and convert user input to integer
    except ValueError:
        feedback_label.config(text="Please enter a valid number.") #Handle non-numeric input
        return

    if isCorrect(user_answer):
        #Correct answer logic
        if ATTEMPT_COUNT == 1:
            SCORE += 10 #10 points for first attempt
            message = "Correct! (+10 points)"
        else:
            SCORE += 5 #5 points for second attempt
            message = "Correct on second try! (+5 points)"
        
        feedback_label.config(text=message, fg="green") #Show success message
        root.after(1000, nextProblem) #Wait 1 second before calling nextProblem
    else:
        #Incorrect answer logic
        ATTEMPT_COUNT += 1 #Increment attempt count
        if ATTEMPT_COUNT > 2:
            #Failed on second attempt (third check)
            feedback_label.config(text=f"Incorrect. The answer was {CURRENT_ANSWER}.", fg="red")
            root.after(1000, nextProblem) #Move to next problem after 1 second
        else:
            #Failed on first attempt, give another try
            feedback_label.config(text="Incorrect. Try again.", fg="red")
            answer_entry.delete(0, END) #Clear the entry field

def isCorrect(user_answer):
    #Check if the user's answer matches the current correct answer
    return user_answer == CURRENT_ANSWER #Returns True or False

def displayResults():
    #Calculate and display the final score and rank
    game_frame.pack_forget() #Hide the game frame
    
    global result_frame #Access the global result frame
    result_frame = Frame(root, padx=20, pady=20) #Create the results frame
    result_frame.pack(padx=10, pady=10) #Display the results frame

    score_percent = (SCORE / (MAX_QUESTIONS * 10)) * 100 #Calculate percentage score

    #Determine rank based on score percentage
    if score_percent > 90:
        rank = "A+"
    elif score_percent > 75:
        rank = "A"
    elif score_percent > 60:
        rank = "B"
    elif score_percent > 40:
        rank = "C"
    else:
        rank = "D"

    #Display results
    Label(result_frame, text="Quiz Complete!", font=("Arial", 18, "bold")).pack(pady=10)
    Label(result_frame, text=f"Final Score: {SCORE} / {MAX_QUESTIONS*10}", font=("Arial", 14)).pack(pady=5)
    Label(result_frame, text=f"Percentage: {score_percent:.0f}%", font=("Arial", 14)).pack(pady=5)
    Label(result_frame, text=f"Your Rank: {rank}", font=("Arial", 16, "bold"), fg="blue").pack(pady=10)

    #Prompt to play again
    Label(result_frame, text="Play again?", font=("Arial", 12)).pack(pady=10)
    Button(result_frame, text="Yes", command=displayMenu).pack(padx=10, pady=10) #Button to restart

displayMenu() #Start the program by showing the difficulty menu
root.mainloop() #Start the Tkinter event loop

    
    
    
    
    
    
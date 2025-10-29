from tkinter import * #Import all names from tkinter directly  

class Student: #Define a class to hold and calculate student data.
    MAX_COURSEWORK = 60 #Define max mark for three coursework components
    MAX_EXAM = 100 #Define max mark for the examination.
    MAX_TOTAL = 160 #Define max overall possible mark 

    def __init__(self, code, name, m1, m2, m3, exam): #Initialize a student object.
        self.code = code #Store student code 
        self.name = name #Store student name 
        self.coursework_marks = [m1, m2, m3] #Store individual coursework marks.
        self.exam_mark = exam #Store examination mark.
        self.total_coursework = sum(self.coursework_marks) #Calculate total coursework mark (out of 60).
        self.total_score = self.total_coursework + self.exam_mark #Calculate total overall score (out of 160).
        self.percentage = (self.total_score / self.MAX_TOTAL) * 100 #Calculate overall percentage.
        self.grade = self._calculate_grade() #Determine the student's grade.

    def _calculate_grade(self): #Internal method to determine the letter grade.
        if self.percentage >= 70: return 'A' #A for 70%+.
        elif self.percentage >= 60: return 'B' #B for 60-69%.
        elif self.percentage >= 50: return 'C' #C for 50-59%.
        elif self.percentage >= 40: return 'D' #D for 40-49%.
        else: return 'F' #F for under 40%.

    def get_display_info(self): #Formats student data into a display string.
        return ( #Return a formatted multiline string.
            f"Name: {self.name}\n" #Student Name.
            f"Code: {self.code}\n" #Student Number.
            f"Total Coursework Mark: {self.total_coursework} / {self.MAX_COURSEWORK}\n" #Total Coursework Mark.
            f"Exam Mark: {self.exam_mark} / {self.MAX_EXAM}\n" #Exam Mark.
            f"Overall Percentage: {self.percentage:.2f}%\n" #Overall Percentage (2 decimal places).
            f"Student Grade: {self.grade}\n" #Final Grade.
        )



class StudentDataApp: #Main application class.
    
    def __init__(self, master): #Initialize the application GUI.
        self.master = master #Store the root Tk window.
        master.title("Student Data Manager") #Set the window title.

        self.students = self._load_data() #Load and parse the student data.
        self.total_students = len(self.students) #Store the total number of students.

        self.create_menu(master) #Create the menu buttons and search area.
        self.create_output_area(master) #Create the text area for output.
        
        #Display initial loading message based on success/failure
        if self.total_students == 0: #Check if data loading failed
            self.output.insert(END, "\n--- ERROR ---\nCould not load data from studentMarks.txt. File may be missing or empty.")
        else:
            self.output.insert(END, f"\nLoaded {self.total_students} student records successfully.")


    def _load_data(self): #Function to read and parse from the external file.
        students_list = [] #Initialize an empty list for Student objects.
        file_path = "studentMarks.txt" #Define the name of the file to read.
        
        try: #Attempt to open and read the file content.
            with open(file_path, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError: #Handle case where file is missing.
            print(f"Error: File '{file_path}' not found.")
            return students_list #Return empty list on failure.

        #Process the lines (skipping the first line which is the count)
        for line in lines[1:]: #Loop through data lines, ignoring the first line (count).
            line = line.strip() #Clean up whitespace.
            if not line: #Skip empty lines.
                continue
            try:
                parts = [p.strip() for p in line.split(',')] #Split by comma.
                code = int(parts[0]) #Student code.
                name = parts[1] #Student name.
                #Ensure we have 4 marks (m1, m2, m3, exam)
                if len(parts) >= 6: #Check for the correct number of fields.
                    marks = [int(m) for m in parts[2:]] #Marks list.
                    students_list.append(Student(code, name, marks[0], marks[1], marks[2], marks[3])) #Create Student object.
                else:
                    print(f"Warning: Skipping line due to insufficient data: {line}") #Log warning for malformed line.
            except ValueError: #Handle cases where marks or code are not integers.
                print(f"Warning: Skipping line due to data format error: {line}")
            except Exception as e: #Catch any other unexpected errors.
                print(f"An unexpected error occurred while processing line: {line}. Error: {e}")
                continue
                
        return students_list #Return the list of Student objects.

    def create_menu(self, master): #Creates the menu buttons and fixed entry box in two rows.
        
        menu_frame = Frame(master) #Create the first frame for main buttons.
        menu_frame.pack(side=TOP, fill=X, padx=10, pady=5) #Place frame at the top.

        Button(menu_frame, text="1. View All", command=self.view_all_records).pack(side=LEFT, padx=5) #View All button.
        Button(menu_frame, text="3. Highest Score", command=self.show_highest_score).pack(side=LEFT, padx=5) #Highest Score button.
        Button(menu_frame, text="4. Lowest Score", command=self.show_lowest_score).pack(side=LEFT, padx=5) #Lowest Score button.
        
       
        search_frame = Frame(master) #Create the second frame for search components.
        search_frame.pack(side=TOP, fill=X, padx=10, pady=(0, 5)) #Place frame just below the menu_frame.
        
        Label(search_frame, text="Code/Name:").pack(side=LEFT, padx=(5, 2)) #Label for input.
        self.search_entry = Entry(search_frame, width=15) #Fixed entry box widget.
        self.search_entry.pack(side=LEFT, padx=(0, 5)) #Place entry box.
        
        Button(search_frame, text="Search", command=self.view_individual_record).pack(side=LEFT, padx=5) #Search button.
    
    def create_output_area(self, master): #Creates the Text widget for results display.
        self.output = Text(master, wrap=WORD, width=60, height=25, font=("Courier", 10)) #Create Text widget.
        self.output.pack(padx=10, pady=10) #Place output area.
        self.output.insert(END, "Student Data Manager Loaded.") #Initial message.

    def clear_output(self, title): #Helper to clear output and set title.
        self.output.delete(1.0, END) #Delete all content.
        self.output.insert(END, f"--- {title} ---\n\n") #Insert the section title.

    def format_student_output(self, student, include_separator=True): #Helper to format a student's info string.
        output = student.get_display_info() #Get the formatted student info.
        if include_separator: #Add separator line if requested.
            output += "---------------------------------------\n"
        return output #Return the formatted string.

    

    def view_all_records(self): #Handler for Option 1: View all student records.
        self.clear_output("All Student Records") #Clear screen.
        total_percentage_sum = 0 #Initialize sum.
        
        for student in self.students: #Loop through every student.
            self.output.insert(END, self.format_student_output(student)) #Output student details.
            total_percentage_sum += student.percentage #Sum percentages.
        
        average_percentage = total_percentage_sum / self.total_students if self.total_students else 0 #Calculate average.

        self.output.insert(END, "\n--- Summary ---\n") #Summary header.
        self.output.insert(END, f"Total Students in Class: {self.total_students}\n") #Total students count.
        self.output.insert(END, f"Average Percentage Mark: {average_percentage:.2f}%\n") #Average percentage.
        self.output.see(END) #Scroll to the bottom.

    def view_individual_record(self): #Handler for Option 2: View individual student record.
        selection = self.search_entry.get() #Get value from the fixed entry box.
        
        if selection: #Proceed only if input is provided.
            self._display_selected_student(selection.strip()) #Call helper function.
            self.search_entry.delete(0, END) #Clear the entry box after search.
        else:
            self.output.insert(END, "\n--- Error ---\nPlease enter a Student Code or Name in the search box.\n") #Error if box is empty.

    def _display_selected_student(self, selection): #Helper to find and display one student.
        self.clear_output("Individual Student Record") #Clear screen.
        selected_student = None #Initialize result.

        try: #1. Try to select by Student Code (int).
            code = int(selection)
            selected_student = next((s for s in self.students if s.code == code), None)
        except ValueError: #2. If not a number, try by Name (partial, case-insensitive).
            name_lower = selection.lower()
            selected_student = next((s for s in self.students if name_lower in s.name.lower()), None)

        if selected_student: #If student is found.
            self.output.insert(END, self.format_student_output(selected_student, include_separator=False))
        else: #If not found.
            self.output.insert(END, f"Error: Student '{selection}' not found by code or name.")
        self.output.see(END) #Scroll to the bottom.

    def show_highest_score(self): #Handler for Option 3.
        self._show_extreme_score(is_highest=True) #Call generic function for highest.

    def show_lowest_score(self): #Handler for Option 4.
        self._show_extreme_score(is_highest=False) #Call generic function for lowest.

    def _show_extreme_score(self, is_highest): #Generic handler for highest/lowest.
        if not self.students: #Check for empty data.
            self.clear_output("No Data")
            self.output.insert(END, "No student data loaded.")
            return

        key_func = lambda s: s.total_score #Define key for comparison (total score).
        
        if is_highest: #Find maximum score student.
            student = max(self.students, key=key_func)
            self.clear_output("Student with Highest Total Score")
        else: #Find minimum score student.
            student = min(self.students, key=key_func)
            self.clear_output("Student with Lowest Total Score")

        self.output.insert(END, self.format_student_output(student, include_separator=False))
        self.output.see(END) #Scroll to the bottom.

root = Tk() #Create the main Tkinter window.
app = StudentDataApp(root) #Initialize the application.
root.mainloop() #Start the Tkinter event loop.
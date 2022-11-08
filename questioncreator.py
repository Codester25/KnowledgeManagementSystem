from tkinter.ttk import Treeview
import tkinter as tk
from tkinter import ANCHOR, StringVar, Toplevel, ttk
import sqlite3
from tkinter import messagebox, W

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()  
    

class employeeCreator(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)       

        # variables for database
        NAME = tk.StringVar()
        AGE = tk.StringVar()
        GENDER = tk.StringVar()        
        PHONE = tk.StringVar()

        # Entries Frame
        frameCreator = tk.Frame(self, bg="grey")
        frameCreator.pack(side=tk.TOP, fill='x')

        # Titel for Employee Page
        title = tk.Label(frameCreator, text="Employee Creator", font=("Comic Sans MS", 18, "bold"), bg="grey", fg="white")
        title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")


        # Labels for employees
        Name = tk.Label(frameCreator, text="Name", font=("Comic Sans MS", 16), bg="grey", fg="white")
        Name.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        Age = tk.Label(frameCreator, text="Age", font=("Comic Sans MS", 16), bg="grey", fg="white")
        Age.grid(row=1, column=2, padx=10, pady=10, sticky="w")        
        Gender = tk.Label(frameCreator, text="Gender", font=("Comic Sans MS", 16), bg="grey", fg="white")
        Gender.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        Phone = tk.Label(frameCreator, text="Phone Number", font=("Comic Sans MS", 16), bg="grey", fg="white")
        Phone.grid(row=3, column=2, padx=10, pady=10, sticky="w")
        filler = tk.Label(self, bg="grey", fg="white")
        filler.pack(side="bottom", fill="both", expand=True)

        # entry Form
        textName = tk.Entry(frameCreator, textvariable=NAME, font=("Comic Sans MS", 16), width=30)
        textName.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        textAge = tk.Entry(frameCreator, textvariable=AGE, font=("Comic Sans MS", 16), width=30)
        textAge.grid(row=1, column=3, padx=10, pady=10, sticky="w")        
        textPhone = tk.Entry(frameCreator, textvariable=PHONE, font=("Comic Sans MS", 16), width=30)
        textPhone.grid(row=3, column=3, padx=10, sticky="w")  

        # gender select drop down
        comboGender = ttk.Combobox(frameCreator, font=("Comic Sans MS", 16), width=28, textvariable=GENDER, state="readonly")
        comboGender['values'] = ("Male", "Female")
        comboGender.grid(row=3, column=1, padx=10, sticky="w")  


        # create the employee table
        con = sqlite3.connect('quizCreator.db')
        cur = con.cursor()            
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS employees(
                        EmployeeID Integer Primary Key,
                        name TEXT,
                        age TEXT,                        
                        gender TEXT,
                        Phone TEXT
                    )
                    """)
        con.commit()


        # insert query function
        def insert(NAME, AGE, GENDER, PHONE):
            cur.execute("INSERT into employees VALUES (NULL, ?, ?, ?, ?)", (NAME, AGE, GENDER, PHONE))
            con.commit()

        # obtain employee data for table
        def fetch():
            cur.execute("SELECT * FROM employees")
            rows = cur.fetchall()
            # #print(rows)
            return rows        

        # update a employee from user inputs
        def update(NAME, AGE, GENDER, PHONE):
            cur.execute("UPDATE employees SET name=?, age=?, gender=?, phone=? WHERE EmployeeID=?", (NAME, AGE, GENDER, PHONE, EmployeeID))
            con.commit()

        # assign employee ID a variable
        def getData(event):
            selected_row = tree.focus()
            data = tree.item(selected_row)
            global EmployeeID
            EmployeeID = data["values"][0]
            #print(EmployeeID)

        # refresh the table so it does not repeat data
        def refreshData():
            tree.delete(*tree.get_children())
            for row in fetch():
                tree.insert("", tk.END, values=row)

        # submit button function
        def submitEmployee():
            if textName.get() == "" or textAge.get() == "" or comboGender.get() == "" or textPhone.get() == "":
                messagebox.showinfo("Input Error", "Please Fill All the Details")
                return
            insert(textName.get(), textAge.get(), comboGender.get(), textPhone.get())
            messagebox.showinfo("Success", "Employee was submitted successfully")
            clearData()
            refreshData()

        # update selected employee to the table with the new entry data
        def updateEmployee():
            if textName.get() == "" or textAge.get() == "" or comboGender.get() == "" or textPhone.get() == "":
                messagebox.showinfo("Input Error", "Please Fill All the Details")
                return
            update(textName.get(), textAge.get(), comboGender.get(), textPhone.get())
            messagebox.showinfo("Success!!", "Employee was updated")
            clearData()
            refreshData()

        # delete employee function
        def deleteEmployee():
            # alert box
            response = messagebox.askyesno("This will delete entire quiz.", "Are you sure you want to proceed?")
            
            # message box yes condition
            if response == 1:  
                messagebox.showinfo("Success", "You have deleted the Employee from the Database")
                #print(EmployeeID)
                cur.execute("DELETE FROM employees WHERE EmployeeID= ?", [EmployeeID])
                con.commit()
                clearData()
                refreshData()

        # reset input to null
        def clearData():
            NAME.set("")
            AGE.set("")            
            GENDER.set("")            
            PHONE.set("")
            
        # Employee table                
        tree = Treeview(frameCreator, columns=(1, 2, 3, 4, 5))
        tree.heading("1", text="Employee EmployeeID")
        tree.column("1", width=5)
        tree.heading("2", text="Name")
        tree.heading("3", text="Age")
        tree.column("3", width=5)
        tree.heading("4", text="Gender")
        tree.column("4", width=10)
        tree.heading("5", text="Phone")
        tree['show'] = 'headings'        
        tree.bind("<ButtonRelease-1>", getData)
        tree.grid(row=4, column=0, columnspan= 5, sticky="ew",pady=10, padx=10)         

        # buttons         
        submitButton = tk.Button(frameCreator, text="Submit Employee", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="green", bd=0, command=submitEmployee)
        submitButton.grid(row=5, column=0, pady=10, padx=10)
        updateButton = tk.Button(frameCreator, text="Update Employee", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="blue", bd=0, command=updateEmployee)
        updateButton.grid(row=5, column=1, pady=10, padx=10)
        deleteButton = tk.Button(frameCreator, text="Delete Employee", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="red", bd=0, command=deleteEmployee)
        deleteButton.grid(row=5, column=2, pady=10, padx=10)
        
        refreshData()

class assignPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        frameCreator = tk.Frame(self, bg="grey")
        frameCreator.pack(side=tk.TOP, fill='x')

        # assignment page title
        title = tk.Label(frameCreator, text="Assignment Page", font=("Comic Sans MS", 18, "bold"), bg="grey", fg="white")
        title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")
        filler = tk.Label(self, bg="grey", fg="white")
        filler.pack(side="bottom", fill="both", expand=True)

        textEmployeeTableTitle = tk.Label(frameCreator, text="Select Employee", font=('Comic Sans MS', 16), bg="grey", fg="white")
        textEmployeeTableTitle.grid(row=1, column=0,  columnspan=2, pady=10, padx=10)
        textQuizTableTitle = tk.Label(frameCreator, text="Select Quiz", font=('Comic Sans MS', 16), bg="grey", fg="white")
        textQuizTableTitle.grid(row=1, column=3,  pady=10, padx=10)
        textAssignmentTableTitle = tk.Label(frameCreator, text="Assignment Table", font=('Comic Sans MS', 16), bg="grey", fg="white")
        textAssignmentTableTitle.grid(row=3, column=0, pady=10, padx=10)
        
        # create assignment table to store selected data.
        con = sqlite3.connect('quizCreator.db')
        cur = con.cursor()            
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS assign (
                    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                    EmployeeID INTEGER NOT NULL,
                    quiz_id INTEGER NOT NULL,
                    FOREIGN KEY(EmployeeID) REFERENCES employees (EmployeeID)
                    ON DELETE NO ACTION
                    ON UPDATE NO ACTION,
                    FOREIGN KEY(quiz_id) REFERENCES Quizes (quiz_id)
                    ON DELETE NO ACTION
                    ON UPDATE NO ACTION
                    )
                    """)
        cur.execute("PRAGMA foreign_keys = ON")
        con.commit()        
                
        # display button shows what is in the tables database
        def showQuizData():
            conn = sqlite3.connect('quizCreator.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM `Quizes`")
            rows = cur.fetchall()    
            for row in rows:
                #print(row) 
                quizTree.insert("", tk.END, values=row)  
            conn.close()
        
        def showEmployeeData():
            conn = sqlite3.connect('quizCreator.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM `employees`")
            rows = cur.fetchall()    
            for row in rows:
                #print(row) 
                employeeTree.insert("", tk.END, values=row)  
            conn.close()

        # removed selection so the input does not happen multiple times
        def refreshSelection():
            for x in employeeTree.selection():
                employeeTree.selection_remove(x)
            for y in quizTree.selection():
                quizTree.selection_remove(y)  
        
        def showAssignData():
            conn = sqlite3.connect('quizCreator.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM `assign`")
            rows = cur.fetchall() 
            assignTree.delete(*assignTree.get_children())   
            for row in rows:
                #print(row) 
                assignTree.insert("", tk.END, values=row)  
            conn.close()        
        
        # insert query function
        def insert(employeeID, quizID):
            cur.execute("INSERT into assign VALUES (NULL, ?, ?)", (employeeID, quizID))
            con.commit()

        # getting EMPloyee ID as a variable
        def getEmployeeData(event):
            selected_row = employeeTree.focus()
            data = employeeTree.item(selected_row)
            global employeeID
            employeeID = data["values"][0]
            #print(employeeID)

        # getting quiz ID as a variable
        def getQuizData(event):
            selected_row = quizTree.focus()
            data = quizTree.item(selected_row)
            global quizID
            quizID = data["values"][0]
            #print(quizID)
        
        # getting assignment ID as a variable
        def getAssignData(event):
            selected_row = assignTree.focus()
            data = assignTree.item(selected_row)
            global assignID
            assignID = data["values"][0]
            #print(assignID)

        # assign button function        
        def assign():            
            insert(employeeID, quizID)
            messagebox.showinfo("Success!!", "Employee was successfully assigned quiz selected.")
            showAssignData()
            refreshSelection() 

        #delete button function
        def deleteAssign():
            # alert box
            response = messagebox.askyesno("This will remove the assignment.", "Are you sure you want to proceed?")
            
            # message box yes condition
            if response == 1:  
                x = assignTree.selection()                
                messagebox.showinfo("Success", "You have removed the Assignment")
                #print(assignID)
                cur.execute("DELETE FROM assign WHERE assignment_id = ?", [assignID])                
                con.commit()           
                for record in x:
                    assignTree.delete(record)

        # Employee tree
        employeeTree = Treeview(frameCreator, column=("c1", "c2"), show='headings')
        employeeTree.column("#1", anchor=tk.CENTER)
        employeeTree.heading("#1", text="Employee ID")
        employeeTree.column("#2", anchor=tk.CENTER)
        employeeTree.heading("#2", text="Employee Name")     
        employeeTree.bind("<ButtonRelease-1>", getEmployeeData)                
        employeeTree.grid(row=2, column=0, padx=20, pady=20, columnspan=2)

        # quiz tree
        quizTree = Treeview(frameCreator, column=("c1", "c2"), show='headings')
        quizTree.column("#1", anchor=tk.CENTER)
        quizTree.heading("#1", text="Quiz Number")
        quizTree.column("#2", anchor=tk.CENTER)
        quizTree.heading("#2", text="Quiz Name")        
        quizTree.bind("<ButtonRelease-1>", getQuizData)             
        quizTree.grid(row=2, column=3, padx=20, pady=20, columnspan=2)

        # buttons        
        assignButton = tk.Button(frameCreator, text="Assign Quiz", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="green", command=assign)
        assignButton.grid(row=2, column=5, padx=10, pady=10)
        deleteAssignmentButton = tk.Button(frameCreator, text="Remove Assignment", width=20, font=("Comic Sans MS", 16, "bold"), fg="white", bg="red", command=deleteAssign)
        deleteAssignmentButton.grid(row=4, column=3, padx=10, pady=10, sticky="s")

        # assign tree
        assignTree = Treeview(frameCreator, column=("c1", "c2", "c3"), show='headings')
        assignTree.column("#1", anchor=tk.CENTER)
        assignTree.heading("#1", text="Assignment ID")
        assignTree.column("#2", anchor=tk.CENTER)
        assignTree.heading("#2", text="Employee Number")  
        assignTree.column("#3", anchor=tk.CENTER)
        assignTree.heading("#3", text="Quiz Number")   
        assignTree.bind("<ButtonRelease-1>", getAssignData)                  
        assignTree.grid(row=4, column=0, columnspan=3, padx=20, pady=20)

        # show database table data
        showEmployeeData()
        showQuizData()
        showAssignData()


class quizPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        frameCreator = tk.Frame(self, bg="grey")
        frameCreator.pack(side=tk.TOP, fill='both') 

        # Quiz title
        title = tk.Label(frameCreator, text="Select a Quiz to View", font=("Comic Sans MS", 18, "bold"), bg="grey", fg="white")
        title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")     
        filler = tk.Label(self, bg="grey", fg="white")
        filler.pack(side="bottom", fill="both", expand=True)
        


        # open quiz button function
        def openQuiz():
            
            newWindow = Toplevel(bg="grey") 
            # Quiz title
            title = tk.Label(newWindow, text=quizName, font=("Comic Sans MS", 24, "bold"), bg="grey", fg="white")
            title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")     
                 
            
            def showQuestion():
                

                conn = sqlite3.connect('quizCreator.db')
                cur = conn.cursor()
                cur.execute("SELECT * FROM `questions` WHERE quiz_id is ?", [quizID])
                rows = cur.fetchall()
                showQuestionData = '' 
                showOptionDataA = ''
                showOptionDataB = ''
                showOptionDataC = ''
                showOptionDataD = ''
                
                #iterate through the data and place in in the variable to show formated quiz
                for row in rows: 
                    #print(row[1])
                    showQuestionData +=  str(row[1]) + "\n" + "\n"
                    
                    showOptionDataA += 'A) ' + str(row[2]) + "\n" + "\n" 
        
                                       
                    showOptionDataB += 'B) ' + str(row[3]) + "\n" + "\n"
                    
                    showOptionDataC += 'C) ' + str(row[4]) + "\n" + "\n"
                    
                    showOptionDataD += 'D) ' + str(row[5]) + "\n" + "\n"   

                QuestionDataLabel = tk.Label(newWindow, text=showQuestionData, font=("Comic Sans MS", 18, "bold"), bg="grey", fg="white", justify="left")
                QuestionDataLabel.grid(row=1, column=0, padx=20, pady=20)
                
                OptionDataLabelA = tk.Label(newWindow, text=showOptionDataA, font=("Comic Sans MS", 18, "bold"), bg="grey", fg="white", justify="left")
                OptionDataLabelA.grid(row=1, column=2, padx=20, pady=20)              
                
                OptionDataLabelB = tk.Label(newWindow, text=showOptionDataB, font=("Comic Sans MS", 18, "bold"), bg="grey", fg="white", justify="left")
                OptionDataLabelB.grid(row=1, column=4, padx=20, pady=20)
                 
                OptionDataLabelC = tk.Label(newWindow, text=showOptionDataC, font=("Comic Sans MS", 18, "bold"), bg="grey", fg="white", justify="left")
                OptionDataLabelC.grid(row=1, column=6, padx=20, pady=20)
                
                OptionDataLabelD = tk.Label(newWindow, text=showOptionDataD, font=("Comic Sans MS", 18, "bold"), bg="grey", fg="white", justify="left")
                OptionDataLabelD.grid(row=1, column=8, padx=20, pady=20) 
                conn.close()   

            #Buttons    
            backButton = tk.Button(newWindow, text="Back", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="Red", command=newWindow.destroy)
            backButton.grid(row=6, column=2, padx=10, pady=10)
            showQuestion()
        # display button shows what is in the tables database
        def showQuizData():
            conn = sqlite3.connect('quizCreator.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM `Quizes`")
            rows = cur.fetchall()    
            for row in rows:
                print(row) 
                quizTree.insert("", tk.END, values=row)  
            conn.close()

        # getting quiz ID as a variable
        def getQuizData(event):
            selected_row = quizTree.focus()
            data = quizTree.item(selected_row)
            global quizID
            global quizName
            quizID = data["values"][0]
            quizName = data["values"][1]
            print(quizID)
            print(quizName)

        # quiz tree
        quizTree = Treeview(frameCreator, column=("c1", "c2"), show='headings')
        quizTree.column("#1", anchor=tk.CENTER)
        quizTree.heading("#1", text="Quiz Number")
        quizTree.column("#2", anchor=tk.CENTER)
        quizTree.heading("#2", text="Quiz Name")        
        quizTree.bind("<ButtonRelease-1>", getQuizData)             
        quizTree.grid(row=1, column=0, padx=20, pady=20, columnspan=3)

        #buttons
        openButton = tk.Button(frameCreator, text="Open Quiz", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="blue", command=openQuiz)
        openButton.grid(row=2, column=2, padx=10, pady=10, sticky="s")

        showQuizData()


class selectedQuizPage(Page):
    def __init__(newWindow, *args, **kwargs):
        Page.__init__(newWindow, *args, **kwargs)

        CORRECT = StringVar
        ANSWERA = StringVar
        ANSWERB = StringVar
        ANSWERC = StringVar
        ANSWERD = StringVar

        frameCreator = tk.Frame(newWindow, bg="grey")
        frameCreator.pack(side=tk.TOP, fill='x')

        # Quiz title
        title = tk.Label(frameCreator, text="Quiz", font=("Comic Sans MS", 18, "bold"), bg="grey", fg="white")
        title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")
        filler = tk.Label(newWindow, bg="grey", fg="white")
        filler.pack(side="bottom", fill="both", expand=True)

        # radio button value controller
        def answerSelect():
            #print('Radiobutton  value :', CORRECT.get())
            if CORRECT == 1:
                CORRECT.set(ANSWERA)
            elif r2 == 2:
                CORRECT.set(ANSWERB)
            elif r2 == 3:
                CORRECT.set(ANSWERC)
            elif r2 == 4:
                CORRECT.set(ANSWERD)
                
        # correct radio
        r1 = tk.Radiobutton(frameCreator, text='A', variable=CORRECT, value='A', font=('Comic Sans MS', 16), bg="grey", fg="white", command=answerSelect)
        r1.grid(row=4, column=1, sticky=W)
        r2 = tk.Radiobutton(frameCreator, text='B', variable=CORRECT, value='B', font=('Comic Sans MS', 16), bg="grey", fg="white",command=answerSelect)
        r2.grid(row=4,column=1, sticky=W, padx=50) 
        r3 = tk.Radiobutton(frameCreator, text='C', variable=CORRECT, value='C', font=('Comic Sans MS', 16), bg="grey", fg="white",command=answerSelect )
        r3.grid(row=4,column=1, sticky=W, padx=100) 
        r4 = tk.Radiobutton(frameCreator, text='D', variable=CORRECT, value='D', font=('Comic Sans MS', 16), bg="grey", fg="white",command=answerSelect )
        r4.grid(row=4,column=1, sticky=W, padx=150) 


# page to create questions for quiz
class questionPage(Page):
    
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # variables
        QUESTION=tk.StringVar()
        ANSWERA=tk.StringVar()
        ANSWERB=tk.StringVar()
        ANSWERC=tk.StringVar()
        ANSWERD=tk.StringVar()
        CORRECT=tk.StringVar()
        QUIZNAME=tk.StringVar()
        QUIZ=tk.IntVar()  

        # references the frame to stack each piece     
        frameCreator = tk.Frame(self, bg="grey")
        frameCreator.pack(side=tk.TOP, fill='x')
        # Title
        title = tk.Label(frameCreator, text="Quiz Creator", font=("Comic Sans MS", 18, "bold"), bg="grey", fg="white")
        title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")
        
        
        # form labels 
        textQuestion = tk.Label(frameCreator, text="Question:", font=('Comic Sans MS', 16), bg="grey", fg="white")
        textQuestion.grid(row=1, column=0,  columnspan=2, sticky='w', pady=10, padx=10)
        textAnswerA = tk.Label(frameCreator, text="Answer A:", font=('Comic Sans MS', 16), bg="grey", fg="white")
        textAnswerA.grid(row=2, column=0,  sticky='w', pady=10, padx=10)
        textAnswerB = tk.Label(frameCreator, text="Answer B:", font=('Comic Sans MS', 16), bg="grey", fg="white")
        textAnswerB.grid(row=3, column=0,  sticky='w', pady=10, padx=10)
        textAnswerC = tk.Label(frameCreator, text="Answer C:", font=('Comic Sans MS', 16), bg="grey", fg="white")
        textAnswerC.grid(row=2, column=2,  sticky='w', pady=10, padx=10)
        textAnswerD = tk.Label(frameCreator, text="Answer D:", font=('Comic Sans MS', 16), bg="grey", fg="white")
        textAnswerD.grid(row=3, column=2,  sticky='w', pady=10, padx=10)
        textCorrect = tk.Label(frameCreator, text="Correct Answer:", font=('Comic Sans MS', 16), bg="grey", fg="white")
        textCorrect.grid(row=4, column=0,  sticky='w', pady=10, padx=10)
        warning = tk.Label(frameCreator, font=("Comic Sans MS", 12))
        warning.grid(row=8)
        checknull = tk.Label(frameCreator, font=("Comic Sans MS", 12))
        checknull.grid(row=11, column=2) 
        
        # user input entered and set to the variables        
        question = tk.Entry(frameCreator, textvariable=QUESTION, relief=tk.FLAT, bd=5, width=60)
        question.grid(row=1, column=1, sticky="w", pady=10, padx=10)
        answerA = tk.Entry(frameCreator, textvariable=ANSWERA, relief=tk.FLAT, bd=5, width=60)
        answerA.grid(row=2, column=1, sticky="w", pady=10, padx=10)
        answerB = tk.Entry(frameCreator, textvariable=ANSWERB, relief=tk.FLAT, bd=5, width=60)
        answerB.grid(row=3, column=1, sticky="w", pady=10, padx=10)
        answerC = tk.Entry(frameCreator, textvariable=ANSWERC, relief=tk.FLAT, bd=5, width=60)
        answerC.grid(row=2, column=3, sticky="w", pady=10, padx=10)
        answerD = tk.Entry(frameCreator, textvariable=ANSWERD, relief=tk.FLAT, bd=5, width=60)
        answerD.grid(row=3, column=3, sticky="w", pady=10, padx=10)

        # sends get data from user input to question table in database  
        def sendData():
            if QUESTION.get() == "" or ANSWERA.get() == "" or ANSWERB.get() == "" or ANSWERC.get() == "" or ANSWERD.get() == ""or CORRECT.get() == "":
                warning.configure(text="All fields must be entered.", fg="red")
            else:
                questionDatabase()
                QUESTION.set("")
                ANSWERA.set("")
                ANSWERB.set("")
                ANSWERC.set("")
                ANSWERD.set("")
                CORRECT.set("")
                warning.configure(text="Question Saved", fg="green")

        # display button shows what is in the tables database
        def showData():
            conn = sqlite3.connect('quizCreator.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM `questions`")
            rows = cur.fetchall()    
            for row in rows:
                #print(row) 
                tree.insert("", tk.END, values=row)  
            conn.close()
        
        # function to send the data with a SQL command
        def questionDatabase():
            conn = sqlite3.connect('quizCreator.db')
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS `questions` 
                        (question_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , 
                        question TEXT, answerA TEXT, answerB TEXT, answerC TEXT, 
                        answerD TEXT, correct TEXT, quiz_id INTEGER, 
                        FOREIGN KEY(quiz_id) REFERENCES Quizes (quiz_id) 
                        ON UPDATE SET NULL
                        ON DELETE SET NULL)""")
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("""INSERT INTO `questions` 
                        (question, answerA, answerB, answerC, answerD, correct, quiz_id) VALUES(?, ?, ?, ?, ?, ?, ?)""", (str(QUESTION.get()), str(ANSWERA.get()), str(ANSWERB.get()), str(ANSWERC.get()), str(ANSWERD.get()), str(CORRECT.get()), str(QUIZ.get())))
            conn.commit()
            cur.close()
            conn.close()

        # radio button value controller
        def answerSelect():
            #print('Radiobutton  value :', CORRECT.get())
            if CORRECT == 1:
                CORRECT.set(ANSWERA)
            elif r2 == 2:
                CORRECT.set(ANSWERB)
            elif r2 == 3:
                CORRECT.set(ANSWERC)
            elif r2 == 4:
                CORRECT.set(ANSWERD)

        # delete selected table item or question if the user messes up.
        def deleteSelected():
            # alert box
            response = messagebox.askyesno("This will delete entire quiz.", "Are you sure you want to proceed?")
            
            # message box yes condition
            if response == 1:
                
                # create selection variable
                x = tree.selection()
                y = tree.item(x)['values'][0]
                #print(y)               
                #print(x)
                # delete display
                for record in x:
                    tree.delete(record)
                
                conn = sqlite3.connect('quizCreator.db')
                cur = conn.cursor()
                cur.execute("DELETE FROM questions WHERE question_id = ?", [y])        
                conn.commit()
                messagebox.showinfo("Success", "You have deleted the question from the Database")
                cur.close()
                conn.close()

        def iterateQUIZ():
            conn = sqlite3.connect('quizCreator.db')
            cur = conn.cursor()
            cur.execute("SELECT oid FROM Quizes ORDER BY oid DESC LIMIT 1;")  
            conn.commit()
            QUIZ.set(cur.fetchone()[0])
            cur.close()
            conn.close()            
            #print(QUIZ.get())

        # sends get data from user input to database
        def createQuiz():
            if QUIZNAME.get() == "":
                checknull.configure(text="Quiz was not Created", fg="red")
            else:
                quizDatabase()  
                QUIZNAME.set("")
                conn = sqlite3.connect('quizCreator.db')
                cur = conn.cursor()
                cur.execute("SELECT oid FROM Quizes ORDER BY oid DESC LIMIT 1;")   
                QUIZ.set([cur.fetchall])                
                conn.commit()
                cur.close()
                conn.close() 
                checknull.configure(text="Quiz Started!", fg="green")
                iterateQUIZ()                

        # popup quiz name 
        def popupQuizName():
            top= tk.Toplevel(self, bg="grey")
            top.geometry("750x250")
            
            # quiz name label
            quizNameLabel = tk.Label(top, text="Please Enter the Quiz Name: ", font=('Comic Sans MS', 16), bg="grey", fg="white")
            quizNameLabel.grid(row=1, column=2, columnspan=2, pady=10)

            # quiz entry form
            quizNameEntry = tk.Entry(top, textvariable=QUIZNAME, relief=tk.FLAT, bd=5, width=60)
            quizNameEntry.grid(row=2, column=2, columnspan=2, pady=10, padx=10)                  

            # quiz name button
            createButton = tk.Button(top, text="Create Quiz", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="green",command=createQuiz)
            createButton.grid(row=3, column=2, pady=10, padx=10, ipadx=10, ipady=10)  
            quitButton = tk.Button(top, text="Quit", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="red",command=top.destroy)   
            quitButton.grid(row=3, column=3, pady=10, padx=10, ipadx=10, ipady=10)
        
        # sends get data from user input to quiz database 
        def quizDatabase():
            conn = sqlite3.connect('quizCreator.db')
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS `Quizes` (quiz_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , quizName VARCHAR(200))")
            cur.execute("INSERT INTO `Quizes` (quizName) VALUES(?)", [str(QUIZNAME.get())])
            conn.commit()
            cur.close()
            conn.close()   
        
        

        # correct radio
        r1 = tk.Radiobutton(frameCreator, text='A', variable=CORRECT, value='A', font=('Comic Sans MS', 16), bg="grey", fg="white", command=answerSelect)
        r1.grid(row=4, column=1, sticky=W)
        r2 = tk.Radiobutton(frameCreator, text='B', variable=CORRECT, value='B', font=('Comic Sans MS', 16), bg="grey", fg="white",command=answerSelect)
        r2.grid(row=4,column=1, sticky=W, padx=50) 
        r3 = tk.Radiobutton(frameCreator, text='C', variable=CORRECT, value='C', font=('Comic Sans MS', 16), bg="grey", fg="white",command=answerSelect )
        r3.grid(row=4,column=1, sticky=W, padx=100) 
        r4 = tk.Radiobutton(frameCreator, text='D', variable=CORRECT, value='D', font=('Comic Sans MS', 16), bg="grey", fg="white",command=answerSelect )
        r4.grid(row=4,column=1, sticky=W, padx=150) 
        CORRECT.set('A') # default radio value

        # create columns and headings for a table to show data
        tree = Treeview(frameCreator, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings')
        tree.column("#1", anchor=tk.CENTER)
        tree.heading("#1", text="Question Number")
        tree.column("#2", anchor=tk.CENTER)
        tree.heading("#2", text="Question")
        tree.column("#3", anchor=tk.CENTER)
        tree.heading("#3", text="A")
        tree.column("#4", anchor=tk.CENTER)
        tree.heading("#4", text="B")
        tree.column("#5", anchor=tk.CENTER)
        tree.heading("#5", text="C")
        tree.column("#6", anchor=tk.CENTER)
        tree.heading("#6", text="D")
        tree.column("#7", anchor=tk.CENTER)
        tree.heading("#7", text="Correct Answer")
        tree.grid(row=9, column=0, columnspan= 5, sticky="ew",pady=10, padx=10)

        # buttons
        submit = tk.Button(frameCreator, text = "Submit Question", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="blue", command=sendData)
        submit.grid(row=7, column= 0)        
        deleteQ = tk.Button(frameCreator, text="Delete Question Selected", width=30, font=("Comic Sans MS", 16, "bold"), fg="white", bg="red", command=deleteSelected)
        deleteQ.grid(row=10, column= 0, columnspan=2, pady=10)
        display = tk.Button(frameCreator, text="Display data", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="orange", command=showData)
        display.grid(row=7, column= 1, pady=10)
        finished = tk.Button(frameCreator, text = "Submit Quiz", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="green", command=popupQuizName)
        finished.grid(row=10, column= 3, pady=10) 
        startquiz = tk.Button(frameCreator, text = "Create New Quiz", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="green", command=popupQuizName)
        startquiz.grid(row=4, column= 3, pady=10)                

        

class SidePanel(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        employeecreator = employeeCreator(self)
        assignpage = assignPage(self)
        quizpage = quizPage(self)
        questionpage = questionPage(self)  

        buttonframe = tk.Frame(self, bg="teal")
        container = tk.Frame(self, bg="grey")
        buttonframe.pack(side="left", fill="y", expand=False)
        container.pack(side="left", fill="both", expand=True)

        employeecreator.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        assignpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        quizpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        questionpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        employeebutton = tk.Button(buttonframe, text="Create Employee", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="green",command=employeecreator.show)
        assignbutton = tk.Button(buttonframe, text="Assign Quiz", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="green",command=assignpage.show)
        viewquiz = tk.Button(buttonframe, text="View Quizes", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="green",command=quizpage.show)
        quizbutton = tk.Button(buttonframe, text="Quiz Creator", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="green",command=questionpage.show)
        exitbutton = tk.Button(buttonframe, text="Exit", width=15, font=("Comic Sans MS", 16, "bold"), fg="white", bg="red",command=self.quit)

        quizbutton.pack(padx=30, ipady=10,expand=True)
        employeebutton.pack(padx=30, ipady=10,expand=True)
        assignbutton.pack(padx=30, ipady=10,expand=True)
        viewquiz.pack(padx=30, ipady=10,expand=True)        
        exitbutton.pack(padx=30, ipady=10,expand=True)
        
        employeecreator.show()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Learning Center Application")
    root.geometry("1650x690")
    main = SidePanel(root)
    main.pack(side="left", fill="both", expand=True)    
    root.mainloop()
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class App():

    def __init__(self, viewActive, viewHistory, addRent, endRent, editRent) -> Tk:
        self.window = Tk()
        self.window.title("Librarian")
        self.window.state('zoomed')

        self.rentData = {}

        ############################## STYLES #########################################
        ### TREE STYLE ###
        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview",
                            background="gray",
                            rowheight=45,
                            fieldbackground='silver',
                            font='Arial, 10')
        treestyle.map('Treeview',
                      background=[('selected', '#2222FF')])

        ############################## TREE FRAME #########################################
        #self.treeFrame = Frame(self.window)
        #self.treeFrame.grid(row=0, column=1, padx=(0, 100), rowspan=5)

        ############################## TREEVIEWS NOTEBOOK #################################
        def switch_to_active_tab(event):
            viewActive()

        def switch_to_history_tab(event):
            viewHistory()

        self.rentsNotebook = ttk.Notebook(self.window)
        
        self.activeTab = Frame(self.rentsNotebook)
        self.historyTab = Frame(self.rentsNotebook)

        self.rentsNotebook.add(self.activeTab, text='Wypożyczenia')
        self.rentsNotebook.add(self.historyTab, text='Historia')
        self.rentsNotebook.bind("<<NotebookTabChanged>>", switch_to_active_tab)
        self.rentsNotebook.bind("<<NotebookTabChanged>>", switch_to_history_tab)
        self.rentsNotebook.grid(row=0, column=1, rowspan=5, sticky=E, pady=20)

        ############################## TREE LABEL #########################################
        self.activeTreeLabel = Label(self.activeTab, text='Aktywne wypożyczenia', font='Arial, 14')
        self.activeTreeLabel.pack(pady=20, anchor=CENTER)

        self.historyTreeLabel = Label(self.historyTab, text='Historia wypożyczeń', font='Arial, 14')
        self.historyTreeLabel.pack(pady=20, anchor=CENTER)

        ############################## ACTIVE TABLE #########################################
        self.activeTreeScroll = Scrollbar(self.activeTab)
        self.activeTreeScroll.pack(side=RIGHT, fill=Y)

        self.activeTable = ttk.Treeview(self.activeTab, yscrollcommand=self.activeTreeScroll.set, selectmode='extended',
                                        columns=('name', 'lastName', 'schoolClass', 'bookTitle', 'rentalDate',
                                                 'maxDate', 'deposit', 'state'),
                                        show='headings')

        self.activeTable.heading('name', text='Imię', anchor=W)
        self.activeTable.heading('lastName', text='Nazwisko', anchor=W)
        self.activeTable.heading('schoolClass', text='Klasa', anchor=CENTER)
        self.activeTable.heading('bookTitle', text='Tytuł książki', anchor=CENTER)
        self.activeTable.heading('rentalDate', text='Data wypożyczenia', anchor=CENTER)
        self.activeTable.heading('maxDate', text='Data do zwrotu', anchor=CENTER)
        self.activeTable.heading('deposit', text='Kaucja', anchor=CENTER)
        self.activeTable.heading('state', text='Status', anchor=CENTER)

        self.activeTable.column("#0", width=0, stretch=NO)
        self.activeTable.column('name', anchor=W, width=200)
        self.activeTable.column('lastName', anchor=W, width=200)
        self.activeTable.column('schoolClass', anchor=CENTER, width=110)
        self.activeTable.column('bookTitle', anchor=CENTER, width=350)
        self.activeTable.column('rentalDate', anchor=CENTER, width=200)
        self.activeTable.column('maxDate', anchor=CENTER, width=200)
        self.activeTable.column('deposit', anchor=CENTER, width=100)
        self.activeTable.column('state', anchor=CENTER, width=150)

        self.activeTable.tag_configure('oddrow', background='white')
        self.activeTable.tag_configure('evenrow', background='lightblue')

        self.activeTreeScroll.config(command=self.activeTable.yview)

        self.activeTable.bind('<Double-1>', editRent)

        self.activeTable.pack(fill='both', expand="yes")

        ############################## HISTORY TABLE #########################################
        self.historyTreeScroll = Scrollbar(self.historyTab)
        self.historyTreeScroll.pack(side=RIGHT, fill=Y)

        self.historyTable = ttk.Treeview(self.historyTab, yscrollcommand=self.historyTreeScroll.set, selectmode='extended',
                                         columns=('name', 'lastName', 'schoolClass', 'bookTitle', 'rentalDate',
                                                  'maxDate', 'returnDate', 'deposit'),
                                         show='headings')

        self.historyTable.heading('name', text='Imię', anchor=W)
        self.historyTable.heading('lastName', text='Nazwisko', anchor=W)
        self.historyTable.heading('schoolClass', text='Klasa', anchor=CENTER)
        self.historyTable.heading('bookTitle', text='Tytuł książki', anchor=CENTER)
        self.historyTable.heading('rentalDate', text='Data wypożyczenia', anchor=CENTER)
        self.historyTable.heading('maxDate', text='Data do zwrotu', anchor=CENTER)
        self.historyTable.heading('returnDate', text='Data zwrotu', anchor=CENTER)
        self.historyTable.heading('deposit', text='Kaucja', anchor=CENTER)

        self.historyTable.column("#0", width=0, stretch=NO)
        self.historyTable.column('name', anchor=W, width=200)
        self.historyTable.column('lastName', anchor=W, width=200)
        self.historyTable.column('schoolClass', anchor=CENTER, width=110)
        self.historyTable.column('bookTitle', anchor=CENTER, width=350)
        self.historyTable.column('rentalDate', anchor=CENTER, width=200)
        self.historyTable.column('maxDate', anchor=CENTER, width=200)
        self.historyTable.column('returnDate', anchor=CENTER, width=200)
        self.historyTable.column('deposit', anchor=CENTER, width=100)

        self.historyTable.tag_configure('oddrow', background='white')
        self.historyTable.tag_configure('evenrow', background='lightblue')

        self.historyTreeScroll.config(command=self.historyTable.yview)

        self.historyTable.pack(fill='both', expand="yes")

        ############################## COMMANDS FRAME #########################################
        self.commandsFrame = Frame(self.window)
        self.commandsFrame.grid(row=0, column=0, padx=20, sticky=W)
        self.commandsFrame['borderwidth'] = 5

        ############################## COMMANDS FRAME LABEL #########################################
        self.commandsFrameLabel = LabelFrame(self.commandsFrame, text='Commands', padx=20, pady=20)
        self.commandsFrameLabel.pack(fill='both', expand="yes")

        ############################## COMMANDS FRAME BUTTONS #########################################
        ### ADD RENT BUTTON ###
        self.addRentBtn = Button(self.commandsFrameLabel, text='Dodaj wypożyczenie', command=addRent)
        self.addRentBtn.pack(pady=10, anchor=CENTER)
        ### END RENT BUTTON ###
        self.endRentBtn = Button(self.commandsFrameLabel, text='Zakończ wypożyczenie', command=endRent)
        self.endRentBtn.pack(pady=10, anchor=CENTER)


class AddRentWindow():

    def __init__(self, root: Tk):
        self.top = Toplevel(root)
        self.top.title('Dodaj wypożyczenie')
        self.top.grab_set()

        self.rentData = None

        ### MAIN FRAME ###
        self.mainFrame = Frame(self.top)
        self.mainFrame.pack()

        ### RENT LABEL ###
        self.addRentLabel = LabelFrame(self.mainFrame, text='Dodawanie wypożyczenia', font='Arial, 9')
        self.addRentLabel.grid(row=0, column=0, padx=20, pady=20)

        ### NAME ###
        self.nameLabel = Label(self.addRentLabel, text='Imię')
        self.nameLabel.grid(row=0, column=0)
        self.nameEntry = Entry(self.addRentLabel)
        self.nameEntry.grid(row=1, column=0, padx=20)

        ### LAST NAME ###
        self.lastNameLabel = Label(self.addRentLabel, text='Nazwisko')
        self.lastNameLabel.grid(row=0, column=1)
        self.lastNameEntry = Entry(self.addRentLabel)
        self.lastNameEntry.grid(row=1, column=1, padx=20)

        ### SCHOOL CLASS ###
        self.schoolClassLabel = Label(self.addRentLabel, text='Klasa')
        self.schoolClassLabel.grid(row=0, column=2)
        self.schoolClassEntry = Entry(self.addRentLabel)
        self.schoolClassEntry.grid(row=1, column=2, padx=20)

        ### BOOK TITLE ###
        self.bookTitleLabel = Label(self.addRentLabel, text='Tytuł książki')
        self.bookTitleLabel.grid(row=2, column=0)
        self.bookTitleEntry = Entry(self.addRentLabel)
        self.bookTitleEntry.grid(row=3, column=0, padx=20, pady=(0, 20))

        ### DEPOSIT ###
        def depositUsed():
            if self.isDepositEnabled.get() is True:
                self.depositEntry.config(state='normal')
            else:
                self.depositEntry.config(state='disabled')

        self.depositLabel = Label(self.addRentLabel, text='Kaucja')
        self.depositLabel.grid(row=5, column=0)
        self.depositEntry = Entry(self.addRentLabel)
        self.depositEntry.grid(row=6, column=0, padx=20, pady=(0, 20))
        self.depositEntry.config(state='disabled')

        self.isDepositEnabled = BooleanVar()
        self.isDepositEnabled.set(False)
        self.depositCheckbox = Checkbutton(self.addRentLabel, text='Wypożyczenie z kaucją?', onvalue=True, offvalue=False,
                                      command=lambda: depositUsed(), variable=self.isDepositEnabled)
        self.depositCheckbox.grid(row=4, column=0)

        ### SUBMIT BUTTON ###
        self.sumbitBtn = ttk.Button(self.addRentLabel, text='Zatwierdź', command=self.getData)
        self.sumbitBtn.grid(row=5, column=2, pady=20, rowspan=2)



    def getData(self):
        global deposit

        name = self.nameEntry.get()
        lastName = self.lastNameEntry.get()
        schoolClass = self.schoolClassEntry.get()
        bookTitle = self.bookTitleEntry.get()

        isValid = False
        if self.isDepositEnabled.get() is True:
            try:
                deposit = int(self.depositEntry.get())
                isValid = True
            except ValueError:
                messagebox.showwarning('Błąd', 'Kaucja musi być liczbą!')
                isValid = False
        else:
            isValid = True
            deposit = 'Brak'

        if isValid is True:
            self.rentData = {"name": name,
                    "lastName": lastName, "schoolClass": schoolClass, "bookTitle": bookTitle, "deposit": deposit}

            messagebox.showinfo('Dodano wypożyczenie', 'Dodano wypożyczenie')
            self.top.destroy()

    def returnData(self):
        return self.rentData
    

class EditRentWindow():

    def __init__(self, root: Tk, rentData: dict):
        self.top = Toplevel(root)
        self.top.title('Edycja wypożyczenia')
        self.top.grab_set()

        self.rentData = None

        ### VARIABLES ###
        self.name = StringVar(value=rentData['name'])
        self.lastName = StringVar(value=rentData['lastName'])
        self.schoolClass = StringVar(value=rentData['schoolClass'])
        self.bookTitle = StringVar(value=rentData['bookTitle'])
        self.deposit = IntVar()
        self.isDepositEnabled = BooleanVar()
        if rentData['deposit'] == 'Brak':
            self.isDepositEnabled.set(False)
        else:
            self.isDepositEnabled.set(True)
            self.deposit.set(int(rentData['deposit']))

        ### MAIN FRAME ###
        self.mainFrame = Frame(self.top)
        self.mainFrame.pack()

        ### WINDOW LABEL ###
        self.windowLabel = LabelFrame(self.mainFrame, text='Edycja wypożyczenia', font='Arial, 9')
        self.windowLabel.grid(row=0, column=0, padx=20, pady=20)
        
        ### NAME ###
        self.nameLabel = Label(self.windowLabel, text='Imię')
        self.nameLabel.grid(row=0, column=0)
        self.nameEntry = Entry(self.windowLabel, textvariable=self.name)
        self.nameEntry.grid(row=1, column=0, padx=20)

        ### LAST NAME ###
        self.lastNameLabel = Label(self.windowLabel, text='Nazwisko')
        self.lastNameLabel.grid(row=0, column=1)
        self.lastNameEntry = Entry(self.windowLabel, textvariable=self.lastName)
        self.lastNameEntry.grid(row=1, column=1, padx=20)

        ### SCHOOL CLASS ###
        self.schoolClassLabel = Label(self.windowLabel, text='Klasa')
        self.schoolClassLabel.grid(row=0, column=2)
        self.schoolClassEntry = Entry(self.windowLabel, textvariable=self.schoolClass)
        self.schoolClassEntry.grid(row=1, column=2, padx=20)

        ### BOOK TITLE ###
        self.bookTitleLabel = Label(self.windowLabel, text='Tytuł książki')
        self.bookTitleLabel.grid(row=2, column=0)
        self.bookTitleEntry = Entry(self.windowLabel, textvariable=self.bookTitle)
        self.bookTitleEntry.grid(row=3, column=0, padx=20, pady=(0, 20))

        ### DEPOSIT ###
        def depositUsed():
            if self.isDepositEnabled.get() is True:
                self.depositEntry.config(state='normal')
                self.depositCheckbox.select()
            else:
                self.depositEntry.config(state='disabled')
                self.depositCheckbox.deselect()

        self.depositLabel = Label(self.windowLabel, text='Kaucja')
        self.depositLabel.grid(row=5, column=0)
        self.depositEntry = Entry(self.windowLabel, textvariable=self.deposit)
        self.depositEntry.grid(row=6, column=0, padx=20, pady=(0, 20))

        self.depositCheckbox = Checkbutton(self.windowLabel, text='Wypożyczenie z kaucją?', onvalue=True, offvalue=False,
                                      command=depositUsed, variable=self.isDepositEnabled)
        self.depositCheckbox.grid(row=4, column=0)

        depositUsed()

        ### SUBMIT BUTTON ###
        self.sumbitBtn = ttk.Button(self.windowLabel, text='Zatwierdź', command=self.getData)
        self.sumbitBtn.grid(row=5, column=2, pady=20, rowspan=2)

    def getData(self):

        name = self.name.get()
        lastName = self.lastName.get()
        schoolClass = self.schoolClass.get()
        bookTitle = self.bookTitle.get()

        isValid = False
        if self.isDepositEnabled.get() is True:
            try:
                deposit = int(self.depositEntry.get())
                isValid = True
            except ValueError:
                messagebox.showwarning('Błąd', 'Kaucja musi być liczbą!')
                isValid = False
        else:
            isValid = True
            deposit = 'Brak'

        if isValid is True:
            self.rentData = {"name": name,
                    "lastName": lastName, "schoolClass": schoolClass, "bookTitle": bookTitle, "deposit": deposit}

            messagebox.showinfo('Zmodyfikowano wypożyczenie', 'Edycja wypożyczenia')
            self.top.destroy()

    def returnData(self):
        return self.rentData

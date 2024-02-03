from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


class App():

    def __init__(self, viewActive, viewHistory) -> Tk:
        self.window = Tk()
        self.window.title("Librarian")
        self.window.state('zoomed')

        self.rentData = {}

        self.columns = {'Imię': 'name', 'Nazwisko': 'lastName', 'Klasa': 'schoolClass', 'Tytuł Książki': 'bookTitle'}

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

        ############################## TREEVIEWS NOTEBOOK #################################

        def switch_tab(event):
            tab = event.widget.tab('current')['text']
            if tab == 'Wypożyczenia':
                viewActive()
            elif tab == 'Historia':
                viewHistory()

        self.rentsNotebook = ttk.Notebook(self.window)

        self.setupActiveTable()
        self.setupHistoryTable()

        self.rentsNotebook.add(self.activeTab, text='Wypożyczenia')
        self.rentsNotebook.add(self.historyTab, text='Historia')
        self.rentsNotebook.bind("<<NotebookTabChanged>>", switch_tab)
        self.rentsNotebook.pack(fill='both', expand='yes', padx=20, pady=20)

    def setupActiveTable(self):
        
        ### ACTIVE TAB ###
        self.activeTab = Frame(self.rentsNotebook)

        ### UI FRAME ###
        self.activeUIFrame = Frame(self.activeTab)
        self.activeUIFrame.pack(side=TOP, fill=X, pady=(0, 10))

        ### FILTER FRAME ###
        self.activeFilterFrame = Frame(self.activeUIFrame)
        self.activeFilterFrame.pack(side=LEFT, fill=X, padx=20, pady=20)

        ### COMMANDS FRAME ###
        self.activeCommandsFrame = Frame(self.activeUIFrame)
        self.activeCommandsFrame.pack(side=RIGHT, fill=X, padx=20, pady=20)

        ### ACTIVE LABEL ###
        self.activeTreeLabel = Label(self.activeFilterFrame, text='Aktywne wypożyczenia', font='Arial, 14')
        self.activeTreeLabel.grid(row=0, column=0, sticky=W, columnspan=2, pady=(0, 20))

        ### FILTER BY COMBOBOX ###
        self.activeFilterBy = ttk.Combobox(self.activeFilterFrame, values=list(self.columns.keys()), state='readonly')
        self.activeFilterBy.grid(row=1, column=0, sticky=W, padx=(0, 7))
        self.activeFilterBy.current(0)
        
        ### FILTER ENTRY ###
        self.activeFilterEntry = Entry(self.activeFilterFrame)
        self.activeFilterEntry.grid(row=1, column=1, sticky=W, padx=(0, 7))

        ### FILTER BUTTON ###
        self.activeFilterBtn = Button(self.activeFilterFrame, text='Filtruj', height=1)  
        self.activeFilterBtn.grid(row=1, column=3, sticky=W)
        
        ### CLEAR FILTER BUTTON ###
        self.activeClearFilterBtn = Button(self.activeFilterFrame, text='Wyczyść', height=1)
        self.activeClearFilterBtn.grid(row=1, column=4, sticky=W, padx=(5, 0))

        ### COMMANDS LABEL ###
        self.commandsLabel = Label(self.activeCommandsFrame, text='Komendy', font='Arial, 14')
        self.commandsLabel.grid(row=0, column=0, sticky=E, pady=(0, 20))

        ### NEW RENT BUTTON ###
        self.newRentBtn = Button(self.activeCommandsFrame, text='Nowe wypożyczenie', width=20) 
        self.newRentBtn.grid(row=1, column=0, sticky=E, pady=(0, 10))

        ### END RENT BUTTON ###
        self.endRentBtn = Button(self.activeCommandsFrame, text='Zakończ wypożyczenie', width=20) 
        self.endRentBtn.grid(row=2, column=0, sticky=E, pady=(0, 10))
        
        ### ACTIVE TREE SCROLLBAR ###
        self.activeTreeScroll = Scrollbar(self.activeTab)
        self.activeTreeScroll.pack(side=RIGHT, fill=Y)

        ############################## ACTIVE TABLE #########################################
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

        self.activeTable.pack(fill='both', expand="yes")

    def setupHistoryTable(self):
        ### HISTORY TAB ###
        self.historyTab = Frame(self.rentsNotebook)

        ### UI FRAME ###
        self.historyUIFrame = Frame(self.historyTab)
        self.historyUIFrame.pack(side=TOP, fill=X, pady=(0, 10))

        ### FILTER FRAME ###
        self.historyFilterFrame = Frame(self.historyUIFrame)
        self.historyFilterFrame.pack(side=LEFT, fill=X, padx=20, pady=20)

        ### TABLE LABEL ###
        self.historyLabel = Label(self.historyFilterFrame, text='Historia', font='Arial, 14')
        self.historyLabel.grid(row=0, column=0, sticky=W, columnspan=2, pady=(0, 20))

        ### FILTER BY COMBOBOX ###
        self.historyFilterBy = ttk.Combobox(self.historyFilterFrame, values=list(self.columns.keys()), state='readonly')
        self.historyFilterBy.grid(row=1, column=0, sticky=W, padx=(0, 7))
        self.historyFilterBy.current(0)

        ### FILTER ENTRY ###
        self.historyFilterEntry = Entry(self.historyFilterFrame)
        self.historyFilterEntry.grid(row=1, column=1, sticky=W, padx=(0, 7))

        ### FILTER BUTTON ###
        self.historyFilterBtn = Button(self.historyFilterFrame, text='Filtruj', height=1)
        self.historyFilterBtn.grid(row=1, column=3, sticky=W)

        ### CLEAR FILTER BUTTON ###
        self.historyClearFilterBtn = Button(self.historyFilterFrame, text='Wyczyść', height=1)
        self.historyClearFilterBtn.grid(row=1, column=4, sticky=W, padx=(5, 0))

        ### HISTORY TREE SCROLLBAR ###
        self.historyTreeScroll = Scrollbar(self.historyTab)
        self.historyTreeScroll.pack(side=RIGHT, fill=Y)

        ############################## HISTORY TABLE #########################################
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

from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class App(Tk):

    def __init__(self, viewActive, viewHistory, addRent, endRent) -> Tk:
        super().__init__()
        self.title("Librarian")
        self.state('zoomed')

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
                      background=[('selected', '#4545d6')])
        ### BUTTON STYLE ###
        buttonStyle = ttk.Style()
        buttonStyle.theme_use('default')
        buttonStyle.configure("TButton",
                              background="silver",
                              font='Arial, 10',
                              relief='flat')

        ############################## TREE FRAME #########################################
        treeFrame = Frame(self)
        treeFrame.grid(row=0, column=1, padx=(0, 100), sticky=E, rowspan=5)

        ############################## TREE LABEL #########################################
        self.treeLabel = Label(treeFrame, text='Aktywne wypożyczenia', font='Arial, 14')
        self.treeLabel.pack(pady=20)

        ############################## TREE SCROLL #########################################
        treeScroll = Scrollbar(treeFrame)
        treeScroll.pack(side=RIGHT, fill=Y)

        ############################## ACTIVE TABLE #########################################
        self.activeTable = ttk.Treeview(treeFrame, yscrollcommand=treeScroll.set, selectmode='extended',
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

        treeScroll.config(command=self.activeTable.yview)

        ############################## HISTORY TABLE #########################################
        self.historyTable = ttk.Treeview(treeFrame, yscrollcommand=treeScroll.set, selectmode='extended',
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

        treeScroll.config(command=self.historyTable.yview)

        ############################## COMMANDS FRAME #########################################
        commandsFrame = Frame(self)
        commandsFrame.grid(row=0, column=0, padx=40, sticky=W)
        commandsFrame['borderwidth'] = 5

        ############################## COMMANDS FRAME LABEL #########################################
        commandsFrameLabel = LabelFrame(commandsFrame, text='Commands', padx=20, pady=20)
        commandsFrameLabel.pack(fill='both', expand="yes")

        ############################## COMMANDS FRAME BUTTONS #########################################
        ### VIEW BUTTONS ###
        viewActiveBtn = ttk.Button(commandsFrameLabel, text='Aktywne wypożyczenia', command=viewActive)
        viewHistoryBtn = ttk.Button(commandsFrameLabel, text='Historia wypożyczeń', command=viewHistory)
        viewActiveBtn.pack(pady=10)
        viewHistoryBtn.pack(pady=10)
        ### ADD RENT BUTTON ###
        addRentBtn = ttk.Button(commandsFrameLabel, text='Dodaj wypożyczenie', command=addRent)
        addRentBtn.pack(pady=10)
        ### END RENT BUTTON ###
        endRentBtn = ttk.Button(commandsFrameLabel, text='Zakończ wypożyczenie', command=endRent)
        endRentBtn.pack(pady=10)

    def addRent(self):

        global data
        data = None

        def getData():
            name = nameEntry.get()
            lastName = lastNameEntry.get()
            schoolClass = schoolClassEntry.get()
            bookTitle = bookTitleEntry.get()
            deposit = depositEntry.get()

            global data
            data = {"name": name,
                    "lastName": lastName, "schoolClass": schoolClass, "bookTitle": bookTitle, "deposit": deposit}

            messagebox.showinfo('Dodano wypożyczenie', 'Dodano wypożyczenie'),
            window.destroy()

            return data

        window = Toplevel(self)
        window.title('Dodaj wypożyczenie')

        ### MAIN FRAME ###
        mainFrame = Frame(window)
        mainFrame.pack()

        ### RENT LABEL ###
        addRentLabel = LabelFrame(mainFrame, text='Dodawanie wypożyczenia', font='Arial, 9')
        addRentLabel.grid(row=0, column=0, padx=20, pady=20)

        ### NAME ###
        nameLabel = Label(addRentLabel, text='Imię')
        nameLabel.grid(row=0, column=0)
        nameEntry = Entry(addRentLabel)
        nameEntry.grid(row=1, column=0, padx=20)

        ### LAST NAME ###
        lastNameLabel = Label(addRentLabel, text='Nazwisko')
        lastNameLabel.grid(row=0, column=1)
        lastNameEntry = Entry(addRentLabel)
        lastNameEntry.grid(row=1, column=1, padx=20)

        ### SCHOOL CLASS ###
        schoolClassLabel = Label(addRentLabel, text='Klasa')
        schoolClassLabel.grid(row=0, column=2)
        schoolClassEntry = Entry(addRentLabel)
        schoolClassEntry.grid(row=1, column=2, padx=20)

        ### BOOK TITLE ###
        bookTitleLabel = Label(addRentLabel, text='Tytuł książki')
        bookTitleLabel.grid(row=2, column=0)
        bookTitleEntry = Entry(addRentLabel)
        bookTitleEntry.grid(row=3, column=0, padx=20, pady=(0, 20))

        ### DEPOSIT ###
        def depositUsed():
            if self.isDepositDisabled.get() is True:
                depositEntry.config(state='normal')
            else:
                depositEntry.config(state='disabled')

        depositLabel = Label(addRentLabel, text='Kaucja')
        depositLabel.grid(row=5, column=0)
        depositEntry = Entry(addRentLabel)
        depositEntry.grid(row=6, column=0, padx=20, pady=(0, 20))
        depositEntry.config(state='disabled')

        self.isDepositDisabled = BooleanVar()
        self.isDepositDisabled.set(False)
        depositCheckbox = Checkbutton(addRentLabel, text='Wypożyczenie z kaucją?', onvalue=True, offvalue=False,
                                      command=lambda: depositUsed(), variable=self.isDepositDisabled)
        depositCheckbox.grid(row=4, column=0)

        ### SUBMIT BUTTON ###
        sumbitBtn = ttk.Button(addRentLabel, text='Zatwierdź', command=getData)
        sumbitBtn.grid(row=5, column=2, pady=20, rowspan=2)

        window.wait_window()
        if data is not None:
            return data

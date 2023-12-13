from tkinter import *
from tkinter import ttk


class App(Tk):

    def __init__(self, viewActive, viewHistory) -> Tk:
        super().__init__()
        self.title("Librarian")
        self.state('zoomed')

        # Treeview style
        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview",
                        background="silver",

                        rowheight=45,
                        fieldbackground='silver',
                        font='Arial, 10')
        treestyle.map('Treeview',
                  background=[('selected', '#4545d6')])

        buttonStyle = ttk.Style()
        buttonStyle.theme_use('default')
        buttonStyle.configure("TButton",
                        background="silver",
                        font='Arial, 10',
                        relief='flat')

        # Add tree frame
        treeFrame = Frame(self)
        treeFrame.grid(row=0, column=1, padx=(0, 100), sticky=E)

        # Add tree scroll
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

        # Add commands frame
        commandsFrame = Frame(self)
        commandsFrame.grid(row=0, column=0, padx=40, sticky=W)
        commandsFrameLabel = LabelFrame(commandsFrame, text='Commands')
        commandsFrameLabel.pack(fill='both', expand="yes", padx=45)
        viewActiveBtn = ttk.Button(commandsFrame, text='Aktywne wypożyczenia', command=viewActive)
        viewHistoryBtn = ttk.Button(commandsFrame, text='Historia wypożyczeń', command=viewHistory)
        viewActiveBtn.pack(pady=10)
        viewHistoryBtn.pack(pady=10)

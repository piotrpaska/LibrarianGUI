#rom tkinter import ttk
#from tkinter import messagebox
from customtkinter import *
import customtkinter
from tkinter import ttk
from PIL import Image, ImageTk


class App():

    def __init__(self, viewActive, viewHistory) -> CTk:
        self.window = CTk()
        self.window.title("Librarian")
        self.window.after(0, lambda: self.window.wm_state('zoomed'))

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.bg_color = self.window._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.text_color = self.window._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        self.btn_color = self.window._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
        print(self.bg_color, self.text_color, self.btn_color)
        # gray17 #DCE4EE #1F6AA5

        self.columns = {'Imię': 'name', 'Nazwisko': 'lastName', 'Klasa': 'schoolClass', 'Tytuł Książki': 'bookTitle'}

        self.currentPage = None
        self.currentButton = None

        def switchPage(page: CTkFrame, button: CTkButton, *optionalFuncs):
            self.currentPage.pack_forget()
            page.pack(fill=BOTH, expand=True, side=RIGHT)
            self.currentPage = page

            self.currentButton.configure(image=self.buttonImages[self.currentButton][0], fg_color='transparent', 
                                         text_color=self.text_color)
            button.configure(image=self.buttonImages[button][1], fg_color='#eeeeee', text_color=self.btn_color)
            self.currentButton = button

            if len(optionalFuncs) > 0:
                for func in optionalFuncs:
                    func()

        ### MENU FRAME ###
        self.sidebarFrame = CTkFrame(self.window, fg_color=self.btn_color, width=220)
        self.sidebarFrame.propagate(0)
        self.sidebarFrame.pack(side=LEFT, fill=Y, anchor=W)

        ### LOGO ###
        logoImg = Image.open('assets/logo.png')
        self.logo = CTkImage(logoImg, logoImg, (170, 170))
        self.logoLabel = CTkLabel(self.sidebarFrame, image=self.logo, text='')
        self.logoLabel.pack(pady=(20, 10), padx=20, anchor=CENTER)

        menuHoverColor = '#14486F'

        ### RENTS TAB SWITCH ###
        rentsIconOff = Image.open('assets/rents-dark.png')
        rentsIconOn = Image.open('assets/rents-dark-highlight.png')
        rentsIconOff = CTkImage(rentsIconOff, rentsIconOff, (30,30))
        rentsIconOn = CTkImage(rentsIconOn, rentsIconOn, (30,30))
        self.rentsTabBtn = CTkButton(self.sidebarFrame, text='Wypożyczenia', hover_color=menuHoverColor, fg_color='transparent',
                                    command=lambda: switchPage(self.activeTabFrame, self.rentsTabBtn, viewActive), 
                                    image=rentsIconOff, compound=LEFT,
                                    font=('Arial Bold', 14), border_color="#3995DC", border_width=2, anchor=W, width=140)
        self.rentsTabBtn.pack(pady=(0, 10), padx=20, ipady=5)

        ### HISTORY TAB SWITCH ###
        historyIconOff = Image.open('assets/history-dark.png')
        historyIconOn = Image.open('assets/history-dark-highlight.png')
        historyIconOff = CTkImage(historyIconOff, historyIconOff, (30,30))
        historyIconOn = CTkImage(historyIconOn, historyIconOn, (30,30))
        self.historyTabBtn = CTkButton(self.sidebarFrame, text='Historia', 
                                       command=lambda: switchPage(self.historyTabFrame, self.historyTabBtn, viewHistory), 
                                       fg_color='transparent', hover_color='#14486F',image=historyIconOff, 
                                       compound=LEFT, font=('Arial Bold', 14), border_color="#3995DC", 
                                       border_width=2, anchor=W, width=140)
        self.historyTabBtn.pack(pady=(0, 10), padx=20, ipady=5)

        self.buttonImages = {
            self.rentsTabBtn: (rentsIconOff, rentsIconOn),
            self.historyTabBtn: (historyIconOff, historyIconOn)
        }

        self.setupActiveTab()
        self.setupHistoryTab()
        self.currentPage = self.activeTabFrame
        self.currentButton = self.rentsTabBtn
        self.activeTabFrame.pack(fill=BOTH, expand=True, side=RIGHT)
        self.rentsTabBtn.configure(image=rentsIconOn, fg_color='#eeeeee', text_color=self.btn_color)

    ############################## ACTIVE TAB SETUP #########################################
    def setupActiveTab(self):

        self.activeTabFrame = CTkFrame(self.window, bg_color=self.bg_color)

        ### UI FRAME ###
        self.activeUIFrame = CTkFrame(self.activeTabFrame)
        self.activeUIFrame.pack(fill=X, pady=(0, 10))

        ### FILTER FRAME ###
        self.activeFilterFrame = CTkFrame(self.activeUIFrame, fg_color='transparent')
        self.activeFilterFrame.pack(side=LEFT, fill=BOTH, padx=15, pady=10)

        ### COMMANDS FRAME ###
        self.activeCommandsFrame = CTkFrame(self.activeUIFrame, fg_color='transparent')
        self.activeCommandsFrame.pack(side=RIGHT, fill=BOTH, padx=15, pady=10)

        ### ACTIVE LABEL ###
        self.activeTreeLabel = CTkLabel(self.activeFilterFrame, text='Aktywne wypożyczenia', font=('Arial', 16))
        self.activeTreeLabel.grid(row=0, column=0, sticky=W, columnspan=2, padx=10, pady=(20, 8))

        ### FILTER BY COMBOBOX ###
        self.activeFilterBy = CTkOptionMenu(self.activeFilterFrame, values=list(self.columns.keys()), state='readonly')
        self.activeFilterBy.grid(row=1, column=0, sticky=W, padx=(10, 7), pady=(0, 20))
        self.activeFilterBy.set(list(self.columns.keys())[0])
        
        ### FILTER ENTRY ###
        self.activeFilterEntry = CTkEntry(self.activeFilterFrame, width=200)
        self.activeFilterEntry.grid(row=1, column=1, sticky=W, padx=(0, 7), pady=(0, 20))

        ### FILTER BUTTON ###
        self.activeFilterBtn = CTkButton(self.activeFilterFrame, text='Filtruj', height=1, width=4)  
        self.activeFilterBtn.grid(row=1, column=3, sticky=W, pady=(0, 20))
        
        ### CLEAR FILTER BUTTON ###
        self.activeClearFilterBtn = CTkButton(self.activeFilterFrame, text='Wyczyść', height=1)
        self.activeClearFilterBtn.grid(row=1, column=4, sticky=W, padx=(5, 20), pady=(0, 20))

        ### COMMANDS LABEL ###
        self.commandsLabel = CTkLabel(self.activeCommandsFrame, text='Komendy', font=('Arial', 16))
        self.commandsLabel.pack(side=TOP, fill=X, padx=10, pady=(10, 8))

        ### NEW RENT BUTTON ###
        self.newRentBtn = CTkButton(self.activeCommandsFrame, text='Nowe wypożyczenie', width=20) 
        self.newRentBtn.pack(side=TOP, fill=X, padx=10, pady=(0, 8))

        ### END RENT BUTTON ###
        self.endRentBtn = CTkButton(self.activeCommandsFrame, text='Zakończ wypożyczenie', width=20) 
        self.endRentBtn.pack(side=TOP, fill=X, padx=10, pady=(0, 10)) 
        
        ### ACTIVE TREE SCROLLBAR ###
        self.activeTreeScroll = CTkScrollbar(self.activeTabFrame)
        self.activeTreeScroll.pack(side=RIGHT, fill=Y)

        ### ACTIVE TABLE ###
        self.activeTable = ttk.Treeview(self.activeTabFrame, yscrollcommand=self.activeTreeScroll.set, selectmode='extended',
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

        self.activeTreeScroll.configure(command=self.activeTable.yview)

        self.activeTable.pack(fill='both', expand="yes")

    ############################## HISTORY TAB SETUP ########################################
    def setupHistoryTab(self):

        self.historyTabFrame = CTkFrame(self.window, bg_color=self.bg_color)

        ### UI FRAME ###
        self.historyUIFrame = CTkFrame(self.historyTabFrame)
        self.historyUIFrame.pack(side=TOP, fill=X, pady=(0, 10))

        ### FILTER FRAME ###
        self.historyFilterFrame = CTkFrame(self.historyUIFrame, fg_color='transparent')
        self.historyFilterFrame.pack(side=LEFT, fill=X, padx=20, pady=20)

        ### TABLE LABEL ###
        self.historyLabel = CTkLabel(self.historyFilterFrame, text='Historia', font=('Arial', 16))
        self.historyLabel.grid(row=0, column=0, sticky=W, columnspan=2, pady=(0, 20))

        ### FILTER BY COMBOBOX ###
        self.historyFilterBy = CTkOptionMenu(self.historyFilterFrame, values=list(self.columns.keys()), state='readonly')
        self.historyFilterBy.grid(row=1, column=0, sticky=W, padx=(0, 7))
        self.historyFilterBy.set(list(self.columns.keys())[0])

        ### FILTER ENTRY ###
        self.historyFilterEntry = CTkEntry(self.historyFilterFrame)
        self.historyFilterEntry.grid(row=1, column=1, sticky=W, padx=(0, 7))

        ### FILTER BUTTON ###
        self.historyFilterBtn = CTkButton(self.historyFilterFrame, text='Filtruj', height=1)
        self.historyFilterBtn.grid(row=1, column=3, sticky=W)

        ### CLEAR FILTER BUTTON ###
        self.historyClearFilterBtn = CTkButton(self.historyFilterFrame, text='Wyczyść', height=1)
        self.historyClearFilterBtn.grid(row=1, column=4, sticky=W, padx=(5, 0))

        ### HISTORY TREE SCROLLBAR ###
        self.historyTreeScroll = CTkScrollbar(self.historyTabFrame)
        self.historyTreeScroll.pack(side=RIGHT, fill=Y)

        ### HISTORY TABLE ###
        self.historyTable = ttk.Treeview(self.historyTabFrame, yscrollcommand=self.historyTreeScroll.set, selectmode='extended',
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

        self.historyTreeScroll.configure(command=self.historyTable.yview)

        self.historyTable.pack(fill='both', expand="yes")

        


class AddRentWindow():

    def __init__(self, root: CTk):
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

    def __init__(self, root: CTk, rentData: dict):
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

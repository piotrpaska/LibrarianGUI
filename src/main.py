from tkinter import *
from tkinter import ttk
import pymongo
import yaml
import ctypes
import datetime
from colorama import Fore, Back, Style

ctypes.windll.shcore.SetProcessDpiAwareness(1)

with open('config.yml', 'r') as yamlFile:
    configFile = yaml.safe_load(yamlFile)

dateFormat = configFile['date_format']

root = Tk()
root.title("Librarian")
root.state('zoomed')

# Treeview style
style = ttk.Style()
style.theme_use('default')
style.configure("Treeview",
                background="silver",

                rowheight=45,
                fieldbackground='silver',
                font=('Arial, 10'))
style.map('Treeview',
          background=[('selected', '#4545d6')])

# Add tree frame
treeFrame = Frame(root)
treeFrame.pack(pady=10)

# Add tree scroll
treeScroll = Scrollbar(treeFrame)
treeScroll.pack(side=RIGHT, fill=Y)

# Add treeview
table = ttk.Treeview(treeFrame, yscrollcommand=treeScroll.set, selectmode='extended', columns=('name', 'lastName', 'schoolClass', 'bookTitle', 'rentalDate', 'maxDate', 'deposit', 'state')
                     ,show='headings')
table.heading('name', text='Imię', anchor=W)
table.heading('lastName', text='Nazwisko', anchor=W)
table.heading('schoolClass', text='Klasa', anchor=CENTER)
table.heading('bookTitle', text='Tytuł książki', anchor=CENTER)
table.heading('rentalDate', text='Data wypożyczenia', anchor=CENTER)
table.heading('maxDate', text='Data zwrotu', anchor=CENTER)
table.heading('deposit', text='Kaucja', anchor=CENTER)
table.heading('state', text='Status', anchor=CENTER)

table.column("#0", width=0, stretch=NO)
table.column('name', anchor=W, width=200)
table.column('lastName', anchor=W, width=200)
table.column('schoolClass', anchor=CENTER, width=110)
table.column('bookTitle', anchor=CENTER, width=350)
table.column('rentalDate', anchor=CENTER, width=200)
table.column('maxDate', anchor=CENTER, width=200)
table.column('deposit', anchor=CENTER, width=200)
table.column('state', anchor=CENTER, width=150)

table.tag_configure('oddrow', background='white')
table.tag_configure('evenrow', background='lightblue')

table.pack()

treeScroll.config(command=table.yview)

# Connect to mongo
client = pymongo.MongoClient(configFile['mongodb_connection_string'])
db = client[configFile['mongo_rents_db_name']]
activeCollection = db[configFile['active_rents_collection_name']]

def viewActiveHires():
    count = 0
    for rent in activeCollection.find():
        # Counting overdue
        maxDateSTR = rent['maxDate']
        if maxDateSTR != '14:10':
            # jeśli kaucja jest wpłacona
            today = datetime.datetime.today().date()
            maxDate = datetime.datetime.strptime(maxDateSTR, dateFormat).date()
            if maxDate < today:
                difference = today - maxDate
                overdue = f'Kara: {difference.days}zł'
            else:
                overdue = f'Wypożyczona'
        else:
            # jeśli kaucja nie została wpłacona
            today = datetime.datetime.today().date()
            rentalDate = datetime.datetime.strptime(rent['rentalDate'], dateFormat).date()
            if rentalDate < today:
                difference = today - rentalDate
                overdue = f'Kara: {difference.days}zł'
            else:
                overdue = f'Wypożyczona'

        if count % 2 == 0:
            table.insert(parent='', index=0,
                         values=(
                             rent['name'],
                             rent['lastName'],
                             rent['schoolClass'],
                             rent['bookTitle'],
                             rent['rentalDate'],
                             rent['maxDate'],
                             rent['deposit'],
                             overdue
                         ), iid=count, tags=('evenrow',))
        else:
            table.insert(parent='', index=0,
                         values=(
                             rent['name'],
                             rent['lastName'],
                             rent['schoolClass'],
                             rent['bookTitle'],
                             rent['rentalDate'],
                             rent['maxDate'],
                             rent['deposit'],
                             overdue
                         ), iid=count, tags=('oddrow',))

        count += 1


viewActiveHires()
root.mainloop()

from librarianLib import *
import pymongo
import yaml
import ctypes
import datetime

ctypes.windll.shcore.SetProcessDpiAwareness(1)

with open('config.yml', 'r') as yamlFile:
    configFile = yaml.safe_load(yamlFile)

dateFormat = configFile['date_format']

# Connect to mongo
client = pymongo.MongoClient(configFile['mongodb_connection_string'])
db = client[configFile['mongo_rents_db_name']]
activeCollection = db[configFile['active_rents_collection_name']]
historyCollection = db[configFile['history_rents_collection_name']]


def viewActiveRents():
    app.historyTable.pack_forget()
    app.activeTable.pack(anchor=E)
    app.activeTable.delete(*app.activeTable.get_children())

    app.treeLabel.config(text='Aktywne wypożyczenia')

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
            app.activeTable.insert(parent='', index=0,
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
            app.activeTable.insert(parent='', index=0,
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


def viewHistoryRents():
    app.activeTable.pack_forget()
    app.historyTable.pack(anchor=E)
    app.historyTable.delete(*app.historyTable.get_children())

    app.treeLabel.config(text='Historia wypożyczeń')

    count = 0
    for rent in historyCollection.find():
        if count % 2 == 0:
            app.historyTable.insert(parent='', index=0,
                                   values=(
                                       rent['name'],
                                       rent['lastName'],
                                       rent['schoolClass'],
                                       rent['bookTitle'],
                                       rent['rentalDate'],
                                       rent['maxDate'],
                                       rent['returnDate'],
                                       rent['deposit'],
                                   ), iid=count, tags=('evenrow',))
        else:
            app.historyTable.insert(parent='', index=0,
                                   values=(
                                       rent['name'],
                                       rent['lastName'],
                                       rent['schoolClass'],
                                       rent['bookTitle'],
                                       rent['rentalDate'],
                                       rent['maxDate'],
                                       rent['returnDate'],
                                       rent['deposit'],
                                   ), iid=count, tags=('oddrow',))

        count += 1


def addRent():
    rentData = app.addRent()
    if rentData is not None:
        rentData['rentalDate'] = str(datetime.datetime.today().strftime(dateFormat))
        if app.isDepositDisabled.get() is True:
            rentData['maxDate'] = str((datetime.datetime.today() + datetime.timedelta(weeks=2)).strftime(dateFormat))
        else:
            rentData['maxDate'] = '14:10'
            rentData['deposit'] = 'Brak'
        print(rentData)
        activeCollection.insert_one(rentData)


def endRent():
    pass


app = App(viewActive=viewActiveRents,
          viewHistory=viewHistoryRents,
          addRent=addRent,
          endRent=endRent)

if __name__ == '__main__':
    viewActiveRents()
    app.mainloop()

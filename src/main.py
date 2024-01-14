from librarianLib import *
from librarianLib.keycloakgui import *
from librarianLib.keycloakfunc import KeycloakLib
import pymongo
import yaml
import ctypes
import datetime
from bson.objectid import ObjectId

# Fixing blurry text on Windows
ctypes.windll.shcore.SetProcessDpiAwareness(1)

################# GLOBAL VARIABLES #################
global app
global token
global keycloakOpenIdLib

################# CONFIG FROM YAML #################
with open('config.yml', 'r') as yamlFile:
    configFile = yaml.safe_load(yamlFile)

dateFormat = configFile['date_format']

keycloakConfig = configFile['keycloak']

################# MONGODB CONNECTION #################
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
                                   ), iid=rent['_id'], tags=('evenrow',))
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
                                   ), iid=rent['_id'], tags=('oddrow',))

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
                                    ), iid=rent['_id'], tags=('evenrow',))
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
                                    ), iid=rent['_id'], tags=('oddrow',))

        count += 1


def addRent():
    rentWindow = AddRentWindow(app.window)
    rentWindow.top.wait_window()
    rentData = rentWindow.returnData()
    if rentData is not None:
        rentData['rentalDate'] = str(datetime.datetime.today().strftime(dateFormat))
        if rentWindow.isDepositEnabled.get() is True:
            rentData['maxDate'] = str((datetime.datetime.today() + datetime.timedelta(weeks=2)).strftime(dateFormat))
        else:
            rentData['maxDate'] = '14:10'
        print(rentData)
        activeCollection.insert_one(rentData)
    else:
        return

    viewActiveRents()
    del rentWindow


def endRent():
    global app
    selected = app.activeTable.selection()
    if len(selected) != 0:
        for i in selected:
            rent = activeCollection.find_one({"_id": ObjectId(i)})
            rent['returnDate'] = str(datetime.datetime.today().strftime(dateFormat))
            historyCollection.insert_one(rent)
            activeCollection.delete_one({'_id': ObjectId(i)})
            messagebox.showinfo('Sukces', 'Wypożyczenie zostało zakończone')
            viewActiveRents()
    else:
        messagebox.showerror('Błąd', 'Nie wybrano żadnego wypożyczenia')


def editRent(event=None):
    global app

    selected = app.activeTable.selection()
    fetchedRent = activeCollection.find_one({"_id": ObjectId(selected[0])})
    editWindow = EditRentWindow(app.window, fetchedRent)
    editWindow.top.wait_window()
    rentData = editWindow.returnData()
    if rentData is not None:
        activeCollection.update_one({'_id': ObjectId(selected[0])}, {'$set': rentData})

    del editWindow


def login():
    global loginWindow
    global token
    loginData = loginWindow.returnData()
    checkLogin = keycloakOpenIdClass.login(loginData['username'], loginData['password'])
    if checkLogin[0] is True and checkLogin is not None:
        token = checkLogin[1]
        loginWindow.top.destroy()
        return True
    else:
        messagebox.showerror('Błąd', 'Niepoprawny login lub hasło')




keycloakOpenIdClass = KeycloakLib(keycloakConfig['server_url'],
                                keycloakConfig['realm_name'],
                                keycloakConfig['openID']['client_id'],
                                keycloakConfig['openID']['client_secret'])

keycloakOpenId = keycloakOpenIdClass.keycloakOpenId

token = None

if __name__ == '__main__':
    loginWindow = LoginWindow(login)
    loginWindow.top.mainloop()

    app = App(viewActive=viewActiveRents,
            viewHistory=viewHistoryRents,
            addRent=addRent,
            endRent=endRent,
            editRent=editRent)

    viewActiveRents()
    app.window.mainloop()

from librarianLib import *
from librarianLib.keycloakgui import *
from librarianLib.keycloakfunc import KeycloakLib
from tkinter import messagebox
import pymongo
import yaml
import ctypes
import datetime
from bson.objectid import ObjectId
import time

# Fixing blurry text on Windows
ctypes.windll.shcore.SetProcessDpiAwareness(1)

################# CONFIG FROM YAML #################
with open('config.yml', 'r') as yamlFile:
    configFile = yaml.safe_load(yamlFile)

dateFormat = configFile['date_format']

keycloakConfig = configFile['keycloak']

viewerRole = configFile['viewer_role_name']
librairanRole = configFile['librarian_role_name']
adminRole = configFile['admin_role_name']

rolesList = [viewerRole, librairanRole, adminRole]

################# MONGODB CONNECTION #################
client = pymongo.MongoClient(configFile['mongodb_connection_string'])
db = client[configFile['mongo_rents_db_name']]
activeCollection = db[configFile['active_rents_collection_name']]
historyCollection = db[configFile['history_rents_collection_name']]


def viewActiveRents():
    global app
    if functionDependentions(0) is False:
        return

    while len(app.rentsTable.get()) > 1:
        app.rentsTable.delete_row(1)
    
    startTime = time.time()
    rents = activeCollection.find()
    print(f'Active rents fetched in {(time.time() - startTime)*1000} ms')
    startTime = time.time()
    for rent in rents:
        ### Counting overdue ###
        maxDateSTR = rent['maxDate']
        if maxDateSTR != '14:10':
            ## If deposit is paid
            today = datetime.datetime.today().date()
            maxDate = datetime.datetime.strptime(maxDateSTR, dateFormat).date()
            if maxDate < today:
                difference = today - maxDate
                overdue = f'Kara: {difference.days}zł'
            else:
                overdue = f'Wypożyczona'
        else:
            ## If deposit is not paid
            today = datetime.datetime.today().date()
            rentalDate = datetime.datetime.strptime(rent['rentalDate'], dateFormat).date()
            if rentalDate < today:
                difference = today - rentalDate
                overdue = f'Kara: {difference.days}zł'
            else:
                overdue = f'Wypożyczona'

        app.rentsTable.add_row(index=1, 
                               values=[rent['name'], 
                               rent['lastName'], 
                               rent['schoolClass'], 
                               rent['bookTitle'], 
                               rent['rentalDate'], 
                               rent['maxDate'], 
                               rent['deposit'], 
                               overdue])
    print(f'Active rents displayed in {(time.time() - startTime)*1000} ms')


def viewHistoryRents():
    global app
    if functionDependentions(0) is False:
        return

    while len(app.historyTable.get()) > 1:
        app.historyTable.delete_row(1)

    for rent in historyCollection.find():
        
        app.historyTable.add_row(index=1, 
                                 values=[rent['name'], 
                                 rent['lastName'], 
                                 rent['schoolClass'], 
                                 rent['bookTitle'], 
                                 rent['rentalDate'], 
                                 rent['maxDate'], 
                                 rent['returnDate'], 
                                 rent['deposit']])


def newRent():
    global app
    if functionDependentions(1) is False:
        return

    rentWindow = AddRentWindow(app.window)
    rentWindow.top.wait_window()
    rentData = rentWindow.returnData()
    if rentData is not None:
        rentData['rentalDate'] = str(datetime.datetime.today().strftime(dateFormat))
        if rentWindow.isDepositEnabled.get() is True:
            rentData['maxDate'] = str((datetime.datetime.today() + datetime.timedelta(weeks=2)).strftime(dateFormat))
        else:
            rentData['maxDate'] = '14:10'
        activeCollection.insert_one(rentData)
    else:
        return

    viewActiveRents()
    del rentWindow


def endRent():
    global app
    if functionDependentions(1) is False:
        return
    
    selected = app.activeTable.selection()
    if len(selected) != 0:
        if messagebox.askyesno('Zakończenie wypożyczenia', 'Czy na pewno chcesz zakończyć wypożyczenie?'):
            for i in selected:
                rent = activeCollection.find_one({"_id": ObjectId(i)})
                rent['returnDate'] = str(datetime.datetime.today().strftime(dateFormat))
                historyCollection.insert_one(rent)
                activeCollection.delete_one({'_id': ObjectId(i)})
                messagebox.showinfo('Sukces', 'Wypożyczenie zostało zakończone')
                viewActiveRents()
        else:
            return
    else:
        messagebox.showerror('Błąd', 'Nie wybrano żadnego wypożyczenia')


def editRent(event=None):
    global app
    if functionDependentions(1) is False:
        return

    selected = app.activeTable.selection()
    fetchedRent = activeCollection.find_one({"_id": ObjectId(selected[0])})
    editWindow = EditRentWindow(app.window, fetchedRent)
    editWindow.top.wait_window()
    rentData = editWindow.returnData()

    if rentData is not None:
        rentData['rentalDate'] = str(datetime.datetime.today().strftime(dateFormat))
        if editWindow.isDepositEnabled.get() is True:
            rentData['maxDate'] = str((datetime.datetime.today() + datetime.timedelta(weeks=2)).strftime(dateFormat))
        else:
            rentData['maxDate'] = '14:10'

        activeCollection.update_one({'_id': ObjectId(selected[0])}, {'$set': rentData})

    del editWindow


def filterActiveRents():
    global app
    if functionDependentions(0) is False:
        return

    while len(app.rentsTable.get()) > 1:
        app.rentsTable.delete_row(1)

    searchPhrase = app.activeFilterEntry.get()
    filterBy = app.columns[app.activeFilterBy.get()]
    if searchPhrase == '':
        messagebox.showerror('Błąd', 'Nie wpisano frazy do wyszukania')
        viewActiveRents()
        return
    else:
        for rent in activeCollection.find({filterBy: { '$regex': searchPhrase, '$options' :'i' }}):
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

            app.rentsTable.add_row(index=1, 
                                    values=[rent['name'], 
                                    rent['lastName'], 
                                    rent['schoolClass'], 
                                    rent['bookTitle'], 
                                    rent['rentalDate'], 
                                    rent['maxDate'], 
                                    rent['deposit'], 
                                    overdue])


def filterHistoryRents():
    global app
    if functionDependentions(0) is False:
        return

    app.historyTable.delete(*app.historyTable.get_children())

    searchPhrase = app.historyFilterEntry.get()
    filterBy = app.columns[app.historyFilterBy.get()]
    if searchPhrase == '':
        messagebox.showerror('Błąd', 'Nie wpisano frazy do wyszukania')
        viewHistoryRents()
        return
    else:
        for rent in historyCollection.find({filterBy: { '$regex': searchPhrase, '$options' :'i' }}):
            app.historyTable.add_row(index=1, 
                                     values=[rent['name'], 
                                     rent['lastName'], 
                                     rent['schoolClass'], 
                                     rent['bookTitle'], 
                                     rent['rentalDate'], 
                                     rent['maxDate'], 
                                     rent['returnDate'], 
                                     rent['deposit']])


def clearFilter():
    global app
    if functionDependentions(0) is False:
        return
    
    tab = app.currentPage
    if tab == app.activeTabFrame:
        app.activeFilterEntry.delete(0, END)
        viewActiveRents()
    elif tab == app.historyTabFrame:
        app.historyFilterEntry.delete(0, END)
        viewHistoryRents()

def functionDependentions(roleLevel: int):
    startTime = time.time()
    print('Checking role...')
    global token
    global app
    global username
    if keycloakLib.checkToken(token) is False:
        messagebox.showerror('Błąd', 'Sesja wygasła')
        app.window.destroy()
        return False
    else:
        if keycloakLib.checkRole(username, roleLevel) is True:
            token = keycloakOpenId.refresh_token(token['refresh_token'])
            print(f'Role checked in {(time.time() - startTime)*1000} ms')
        else:
            messagebox.showerror('Błąd', 'Nie masz uprawnień do tej czynności')
            return False

def login():
    def keycloakLogin():
        nonlocal loginWindow
        loginData = loginWindow.returnData()
        checkLogin = keycloakLib.login(loginData['username'], loginData['password'])
        if checkLogin[0] is True and checkLogin is not None:
            global token
            token = checkLogin[1]
            global username
            username = loginData['username']
            loginWindow.top.destroy()
        else:
            messagebox.showerror('Błąd', 'Niepoprawny login lub hasło')

    loginWindow = LoginWindow(keycloakLogin)
    loginWindow.top.mainloop()


keycloakLib = KeycloakLib(keycloakConfig['server_url'],
                                keycloakConfig['realm_name'],
                                keycloakConfig['openID']['client_id'],
                                keycloakConfig['openID']['client_secret'],
                                keycloakConfig['admin_username'],
                                keycloakConfig['admin_password'],
                                rolesList)

keycloakOpenId = keycloakLib.keycloakOpenId
keycloakAdmin = keycloakLib.keycloakAdmin

token = None

def closeSesisson():

    if messagebox.askyesno('Wylogowywanie', 'Czy na pewno chcesz wyjść z programu?'):
        keycloakOpenId.logout(token['refresh_token'])
        quit()
    else:
        pass


if __name__ == '__main__':

    while True:
        login()

        app = App(viewActive=viewActiveRents,
                viewHistory=viewHistoryRents)
        
        #app.newRentBtn.configure(command=newRent)
        #app.endRentBtn.configure(command=endRent)
        #app.activeTable.bind('<Double-Button-1>', editRent)
        app.activeFilterBtn.configure(command=filterActiveRents)
        app.activeClearFilterBtn.configure(command=clearFilter)
        app.historyFilterBtn.configure(command=filterHistoryRents)
        app.historyClearFilterBtn.configure(command=clearFilter)

        app.window.protocol("WM_DELETE_WINDOW", closeSesisson)
        
        viewActiveRents()
        app.window.mainloop()

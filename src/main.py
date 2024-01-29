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

    app.activeTable.delete(*app.activeTable.get_children())

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
    global app
    if functionDependentions(0) is False:
        return

    app.historyTable.delete(*app.historyTable.get_children())

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


def functionDependentions(roleLevel: int):
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
    keycloakOpenId.logout(token['refresh_token'])
    quit()


if __name__ == '__main__':

    while True:
        login()

        app = App(viewActive=viewActiveRents,
                viewHistory=viewHistoryRents,
                addRent=newRent,
                endRent=endRent,
                editRent=editRent)

        app.window.protocol("WM_DELETE_WINDOW", closeSesisson)

        viewActiveRents()
        app.window.mainloop()

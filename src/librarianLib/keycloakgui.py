from tkinter import *

class LoginWindow():

    def __init__(self, loginFunction) -> None:

        def onClose():
            quit()

        self.top = Tk()
        self.top.title('Logowanie')
        self.top.protocol("WM_DELETE_WINDOW", onClose)

        ### VARIABLES ###
        self.username = StringVar()
        self.password = StringVar()

        ### MAIN FRAME ###
        self.mainFrame = Frame(self.top)
        self.mainFrame.pack(padx=20, pady=20)

        ### NAME LABEL ###
        self.usernameLabel = Label(self.mainFrame, text='Nazwa użytkownika:')
        self.usernameLabel.grid(row=0, column=0, padx=20, sticky=E)

        ### NAME ENTRY ###
        self.usernameEntry = Entry(self.mainFrame, textvariable=self.username)
        self.usernameEntry.grid(row=0, column=1, padx=20, pady=5)

        ### PASSWORD LABEL ###
        self.passwordLabel = Label(self.mainFrame, text='Hasło:')
        self.passwordLabel.grid(row=1, column=0, padx=20, sticky=E)

        ### PASSWORD ENTRY ###
        self.passwordEntry = Entry(self.mainFrame, show='*', textvariable=self.password)
        self.passwordEntry.grid(row=1, column=1, padx=20, pady=5)

        ### LOGIN BUTTON ###
        self.loginButton = Button(self.mainFrame, text='Zaloguj', command=loginFunction)
        self.loginButton.grid(row=2, column=1, padx=20, pady=20)

    def returnData(self):
        return {
            'username': self.usernameEntry.get(),
            'password': self.passwordEntry.get()
        }

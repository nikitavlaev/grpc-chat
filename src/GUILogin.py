from tkinter import Tk, Toplevel, Label, CENTER, Entry, Text, Button, Scrollbar, DISABLED, END, NORMAL, messagebox


class GUILogin:
    def __init__(self):
        # chat window which is currently hidden
        self.name = ""
        self.role = ""
        self.login_layout()
        self.window_destroyed = False

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window_destroyed = True
            self.login.destroy()

    def login_layout(self):
        # login window
        self.login = Tk()
        self.login.protocol("WM_DELETE_WINDOW", self.on_closing)

        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=600,
                             height=250)
        # create a greeting Label
        self.pls = Label(self.login,
                         text="Please login and choose role to continue",
                         justify=CENTER,
                         font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)

        # create a name for role label
        self.labelName = Label(self.login,
                               text="Name: ",
                               font="Helvetica 12")

        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.31)

        # create a entry box for
        # typing the name to login
        self.entryName = Entry(self.login,
                               font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.35)

        # set the focus of the curser
        self.entryName.focus()

        # create a role label
        self.labelName = Label(self.login,
                               text="Role (C or S): ",
                               font="Helvetica 12")

        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.51)

        # create a entry box for
        # typing the role to login
        self.entryRole = Entry(self.login,
                               font="Helvetica 14")

        self.entryRole.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.55)


        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.__set_name_role(self.entryName.get(), self.entryRole.get()))

        self.go.place(relx=0.4,
                      rely=0.75)

        self.login.mainloop()

    def __set_name_role(self, name, role):
        self.name = name
        self.role = role
        self.window_destroyed = True
        self.login.destroy()

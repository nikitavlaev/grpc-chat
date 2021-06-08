from tkinter import Tk, Label, CENTER, Entry, Button, messagebox


class ConnectionInfoRetriever:
    def __init__(self):
        # chat window which is currently hidden
        self.ip = None 
        self.port = None
        self.premature_exit = False
        self.connector_layout()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.premature_exit = True
            self.window.destroy()

    def connector_layout(self):
        # Connection window
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # set the title
        self.window.title("Connection")
        self.window.resizable(width=False,
                             height=False)
        self.window.configure(width=600,
                             height=250)
        # create a greeting Label
        self.pls = Label(self.window,
                         text="Please enter server ip and port to create connection",
                         justify=CENTER,
                         font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.1,
                       rely=0.07)

        # create a name for role label
        self.labelIp = Label(self.window,
                               text="IP: ",
                               font="Helvetica 12")

        self.labelIp.place(relheight=0.2,
                             relx=0.1,
                             rely=0.31)

        # create a entry box for
        # typing the ip
        self.entryIp = Entry(self.window,
                               font="Helvetica 14")

        self.entryIp.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.35)

        # set the focus of the cursor
        self.entryIp.focus()

        # create a role label
        self.labelPort= Label(self.window,
                               text="PORT: ",
                               font="Helvetica 12")

        self.labelPort.place(relheight=0.2,
                             relx=0.1,
                             rely=0.51)

        # create a entry box for
        # typing the port
        self.entryPort = Entry(self.window,
                               font="Helvetica 14")

        self.entryPort.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.55)

        # create a Continue Button
        # along with action
        self.go = Button(self.window,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.__set_ip_port(self.entryIp.get(), self.entryPort.get()))

        self.go.place(relx=0.4,
                      rely=0.75)

        self.window.mainloop()

    def __set_ip_port(self, ip, port):
        self.ip = ip
        self.port = port
        self.window.destroy()

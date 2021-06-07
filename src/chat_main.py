from tkinter import Tk, Label, Entry, Text, Button, Scrollbar, DISABLED, END, NORMAL, messagebox
from dataclasses import dataclass

@dataclass
class ConnectionInfo:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

class Peer:
    def __init__(self, name, ip, port):
            self.name = name
            self.con_info = ConnectionInfo(ip, port)

    def establish_connection(self):
        pass

class ChatMain:
    def __init__(self, name, chat):
        # chat window which is currently hidden
        self.name = name
        self.chat = chat
        self.Window = Tk()
        self.layout()

    def run(self):
        self.Window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.Window.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.Window.destroy()

    # The main layout of the chat
    def layout(self):
        # to show chat window
        self.Window.title("CHATROOM")
        self.Window.resizable(width=True,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = ChatConsole(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.send_button(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    # function to basically start the thread for sending messages
    def send_button(self, text):
        pass

    def send_message(self, text):
        pass

class ChatConsole(Text):
    def display_msg(self, msg):
        self.config(state=NORMAL)
        line = f"[{msg.name}] at [{msg.timestamp.ToDatetime()}]:\n {msg.content}"
        self.insert(END, line + "\n\n")

        self.config(state=DISABLED)
        self.see(END)

from tkinter import DISABLED, END, messagebox
import threading

import grpc

import chat_pb2
import chat_pb2_grpc

from src.chat_main import ChatMain, Peer


class Client(Peer):
    def __init__(self, name, ip, port):
        super(Client, self).__init__(name, ip, port)
        self.establish_connection()
        self.chat = []
        self.gui = GUIClient(name, self.chat, self.conn)
        self.gui.run()

    def establish_connection(self):
        # create a gRPC channel + stub
        self.channel = grpc.insecure_channel(self.con_info.ip + ':' + str(self.con_info.port))
        self.conn = chat_pb2_grpc.ChatStub(self.channel)

        # create new listening thread for when new message streams come in
        threading.Thread(target=self.__receive, daemon=True).start()

    # function to receive messages
    def __receive(self):
        try:
            meta = chat_pb2.Meta()
            meta.name = self.name
            for msg in self.conn.S2C(meta):  # this line will wait for new messages from the server!
                self.gui.textCons.display_msg(msg)
        except grpc.RpcError as rpc_error:  # TODO catch certain exception, not all of them
            print(rpc_error)
            self.gui.on_disconnected()


# GUI class for the client chat
class GUIClient(ChatMain):
    def __init__(self, name, chat, conn):
        super(GUIClient, self).__init__(name, chat)
        self.conn = conn

    # function to basically start the thread for sending messages
    def send_button(self, text):
        self.textCons.config(state=DISABLED)
        self.text = text
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.send_message, kwargs={'text': text})
        snd.start()

    # function to send messages
    def send_message(self, text):
        msg = chat_pb2.Msg()
        msg.name = self.name
        msg.content = text
        msg.timestamp.GetCurrentTime()
        self.textCons.display_msg(msg)
        self.conn.C2S(msg)
        # create a GUI class object

    def on_disconnected(self):
        if messagebox.askokcancel("Quit", f"Server disconnected. Press OK to exit (might take couple of sec)"):
            self.Window.destroy()


if __name__ == '__main__':
    g = GUIClient("Localhost", "", 50051)

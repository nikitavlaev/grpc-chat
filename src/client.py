from tkinter import DISABLED, END, messagebox
import threading

import grpc
from google.protobuf.timestamp_pb2 import Timestamp

import chat_pb2
import chat_pb2_grpc

from src.GUI import GUI


# GUI class for the client chat
class GUIClient(GUI):
    class Client:
        def __init__(self, name, ip, port):
            self.name = name
            self.ip = ip
            self.port = port

    def __init__(self, name, ip, port):
        super(GUIClient, self).__init__(name, ip, port)

    def establish_connection(self, ip, port):
        self.client_data = self.Client(self.name, ip, port)

        # create a gRPC channel + stub
        self.channel = grpc.insecure_channel(self.client_data.ip + ':' + str(self.client_data.port))
        self.conn = chat_pb2_grpc.ChatStub(self.channel)

        # create new listening thread for when new message streams come in
        threading.Thread(target=self.__receive, daemon=True).start()

    # function to basically start the thread for sending messages
    def send_button(self, text):
        self.textCons.config(state=DISABLED)
        self.text = text
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.send_message, kwargs={'text': text})
        snd.start()

    # function to receive messages
    def __receive(self):
        try:
            meta = chat_pb2.Meta()
            meta.name = self.name
            for msg in self.conn.S2C(meta):  # this line will wait for new messages from the server!
                GUI.display_msg(msg, self.textCons)
        except:  # TODO catch certain exception, not all of them
            self.on_disconnected()

    # function to send messages
    def send_message(self, text):
        if not GUIClient.grpc_server_on(self.channel):
            self.on_closing()
        msg = chat_pb2.Msg()
        msg.name = self.name
        msg.content = text
        msg.timestamp.GetCurrentTime()
        GUI.display_msg(msg, self.textCons)
        self.conn.C2S(msg)
        # create a GUI class object

    def on_disconnected(self):
        if messagebox.askokcancel("Quit", f"Server disconnected. Press OK to exit (might take couple of sec)"):
            self.Window.destroy()

    @staticmethod
    def grpc_server_on(channel) -> bool:
        TIMEOUT_SEC = 5
        try:
            grpc.channel_ready_future(channel).result(timeout=TIMEOUT_SEC)
            return True
        except grpc.FutureTimeoutError:
            return False


if __name__ == '__main__':
    g = GUIClient("Localhost", "", 50051)

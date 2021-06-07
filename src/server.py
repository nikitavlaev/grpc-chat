from concurrent import futures
import logging
import socket
from tkinter import DISABLED, END, messagebox, Button, Label
import threading

import grpc

import chat_pb2
import chat_pb2_grpc

from src.chat_main import ChatMain, Peer, ConnectionInfo


class CancelToken:
    fexit = 0

    def cancel(self):
        self.fexit = 1

    def is_cancelled(self):
        return self.fexit > 0

class StopEventService:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def set_all(self):
        for e in self.events:
            e.set()

class Server(Peer):
        def __init__(self, name):
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            port = 50051

            super(Server, self).__init__(name, ip, port)
            self.chat = []
            self.c_token = CancelToken()
            self.gui = GUIServer(name, self.c_token, self.chat, self.con_info)
            self.establish_connection()
            self.gui.run()

        def establish_connection(self):
            def wait_and_stop_server(stop_event):
                stop_event.wait()
                self.grpc_server.stop(1)
            
            hostname = socket.gethostname()
            if self.con_info.ip == '':
                self.con_info.ip = socket.gethostbyname(hostname)

            logging.debug(f"Server name: {self.name}")

            stop_event = threading.Event()
            self.grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            chat_pb2_grpc.add_ChatServicer_to_server(
                Chat(
                    self.chat,
                    self.name,
                    self.c_token,
                    self.gui.textCons,
                ),
                self.grpc_server,
            )

            logging.debug(f"Hostname: {hostname}")
            logging.debug(f"IP Address: {self.con_info.ip}")
            self.grpc_server.add_insecure_port(f'{self.con_info.ip}:{self.con_info.port}')
            self.grpc_server.start()

            self.gui.stop_event_service.add_event(stop_event)
            server_stopper = threading.Thread(target=wait_and_stop_server, kwargs={'stop_event': stop_event})
            server_stopper.start()


class Chat(chat_pb2_grpc.ChatServicer):
        def __init__(self, chat, name, c_token, text_cons):
            self.chat = chat
            self.last_index = 0
            self.c_token = c_token
            self.name = name
            self.textCons = text_cons

        def S2C(self, request, context):
            # For every client a infinite loop starts (in gRPC's own managed thread)
            while True:
                if self.c_token.is_cancelled():
                    context.cancel()
                    break
                # Check if there are any new messages
                while len(self.chat) > self.last_index:
                    msg = self.chat[self.last_index]
                    self.last_index += 1
                    if msg.name != request.name:
                        yield msg
            logging.debug("Finished client session")

        def C2S(self, request, context):
            self.chat.append(request)
            self.textCons.display_msg(request)
            return chat_pb2.Status(code=0)

class GUIServer(ChatMain):
    def __init__(self, name, c_token, chat, con_info):
        self.c_token = c_token
        self.con_info = con_info
        self.stop_event_service = StopEventService()
        super(GUIServer, self).__init__(name, chat)
        self.add_connection_info_button()
    
    def add_connection_info_button(self):
        # create a Display connection info button
        self.buttonConnInfo = Button(self.Window,
                                text="Display connection info",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.display_connection())

        self.buttonConnInfo.place(relx=0.0,
                             rely=0.0,
                             relheight=0.072,
                             relwidth=0.4)

    # function to display connection info window
    def display_connection(self):
        messagebox.showinfo(
            "Connection info",
            f"IP: {self.con_info.ip}, PORT: {self.con_info.port}",
        )

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
        # по ссылке chat сделать полем GUI
        self.chat.append(msg)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.c_token.cancel()
            self.stop_event_service.set_all()
            self.Window.destroy()
            logging.debug("Server finished successfully")

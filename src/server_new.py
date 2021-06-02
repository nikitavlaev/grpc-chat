# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import threading
from concurrent import futures
import socket
from tkinter import DISABLED, NORMAL, END, messagebox

import grpc
from google.protobuf.timestamp_pb2 import Timestamp

import chat_pb2
import chat_pb2_grpc

from src.GUI import GUI


class CancelToken:
    fexit = 0

    def cancel(self):
        self.fexit = 1

    def is_cancelled(self):
        return self.fexit > 0


class GUIServer(GUI):
    class Server:
        def __init__(self, name, ip, port):
            self.name = name
            self.ip = ip
            self.port = port
            self.chat = []

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
            print("out of while")

        def C2S(self, request, context):
            self.chat.append(request)
            GUI.display_msg(request, self.textCons)
            return chat_pb2.Status(code=0)

    def __init__(self, name, ip='', port=50051):
        self.c_token = None
        self.server = None
        super(GUIServer, self).__init__(name, ip, port)

    def establish_connection(self, ip, port):
        hostname = socket.gethostname()
        if ip == '':
            ip = socket.gethostbyname(hostname)

        self.server_data = self.Server(self.name, ip, port)
        print(self.server_data.name)

        self.c_token = CancelToken()

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        chat_pb2_grpc.add_ChatServicer_to_server(self.Chat(self.server_data.chat, self.server_data.name
                                                           , self.c_token, self.textCons), self.server)

        print(f"Hostname: {hostname}")
        print(f"IP Address: {self.server_data.ip}")
        self.server.add_insecure_port(f'{self.server_data.ip}:{self.server_data.port}')
        self.server.start()

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
        GUI.display_msg(msg, self.textCons)
        self.server_data.chat.append(msg)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.server.stop(1)
            self.c_token.cancel()
            self.Window.destroy()
            print("STOPPED")

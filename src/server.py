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
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging
import socket

import grpc
from google.protobuf.timestamp_pb2 import Timestamp

import chat_pb2
import chat_pb2_grpc

class CancelToken():
    fexit = 0

    def cancel(self):
        self.fexit = 1

    def is_cancelled(self):
        return self.fexit > 0

class Chat(chat_pb2_grpc.ChatServicer):

    def __init__(self, chat, name, c_token):
        self.chat = chat
        self.lastindex = 0
        self.c_token = c_token
        self.name = name
    
    def S2C(self, request_iterator, context):
        
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            if self.c_token.is_cancelled():
                context.cancel()
                break

            # Check if there are any new messages
            while len(self.chat) > self.lastindex:
                n = self.chat[self.lastindex]
                self.lastindex += 1
                msg = chat_pb2.Msg()
                msg.name = self.name
                msg.content = n
                msg.timestamp.GetCurrentTime()
                yield msg

        print("out of while")
    
    def C2S(self, request, context):
        self.chat.append(request.content)
        # Bug with msg order here
        # once names are introduced, resolvable
        self.lastindex += 1
        line = f"[{request.name}] at [{request.timestamp.ToDatetime()}]: {request.content}"
        print(line)
        return chat_pb2.Status(code=0)

class Server:
    PORT = 50051

    def __init__(self, name):
        chat = []
        c_token = CancelToken()

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        chat_pb2_grpc.add_ChatServicer_to_server(Chat(chat, name, c_token), server)
        
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"Hostname: {hostname}")
        print(f"IP Address: {ip_address}")
        server.add_insecure_port(f'{ip_address}:{Server.PORT}')
        
        print('Starting server. Listening...')
        server.start()
        try:
            while 1:
                msg = input()
                chat.append(msg)
                # print(chat)
        except:
            server.stop(1)
            c_token.cancel()
            print("STOPPED")


if __name__ == '__main__':
    logging.basicConfig()
    Server.serve()

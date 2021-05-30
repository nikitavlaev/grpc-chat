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

import grpc

import chat_pb2
import chat_pb2_grpc

class CancelToken():
    fexit = 0

    def cancel(self):
        self.fexit = 1

    def is_cancelled(self):
        return self.fexit > 0

class Chat(chat_pb2_grpc.ChatServicer):

    def __init__(self, chat, c_token):
        self.chat = chat
        self.lastindex = 0
        self.c_token = c_token
    
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
                msg.content = n
                yield msg

        print("out of while")
    
    def C2S(self, request, context):
        self.chat.append(request.content)
        # Bug with msg order here
        # once names are introduced, resolvable
        self.lastindex += 1
        print("[{}] {}".format("OTHER:", request.content))
        return chat_pb2.Status(code=0)


def serve():
    chat = []
    c_token = CancelToken()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(Chat(chat, c_token), server)
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while 1:
            msg = input()
            chat.append(msg)
            print(chat)
    except:
        server.stop(1)
        c_token.cancel()
        print("STOPPED")


if __name__ == '__main__':
    logging.basicConfig()
    serve()

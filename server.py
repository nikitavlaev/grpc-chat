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

chat = []

class Chat(chat_pb2_grpc.ChatServicer):
    lastindex = 0

    def S2C(self, request_iterator, context):
        
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            # Check if there are any new messages
            while len(chat) > self.lastindex:
                n = chat[self.lastindex]
                self.lastindex += 1
                msg = chat_pb2.Msg()
                msg.content = n
                yield msg
    
    def C2S(self, request, context):
        chat.append(request.content)
        # Bug with msg order here
        # once names are introduced, resolvable
        self.lastindex += 1
        print("[{}] {}".format("OTHER:", request.content))
        return chat_pb2.Status(code=0)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(Chat(), server)
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while 1:
            msg = input()
            chat.append(msg)
    except:
        server.stop(1)
        print("STOPPED")


if __name__ == '__main__':
    logging.basicConfig()
    serve()

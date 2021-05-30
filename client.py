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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging
import threading

import grpc

import chat_pb2
import chat_pb2_grpc

address = 'localhost'
port = 50051

class Client:
    chat = []

    def __init__(self):
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = chat_pb2_grpc.ChatStub(channel)
        # create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()

        # main loop
        while 1:
            text = input()
            self.chat.append(text)
            msg = chat_pb2.Msg()
            msg.content = text
            self.conn.C2S(msg)

    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        for note in self.conn.S2C(chat_pb2.Empty()):  # this line will wait for new messages from the server!
            print("{} {}".format("OTHER:", note.content))  # debugging statement
            self.chat.append("[{}] {}\n".format("OTHER:", note.content))  # add the message to the UI


if __name__ == '__main__':
    logging.basicConfig()
    c = Client()

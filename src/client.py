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
from google.protobuf.timestamp_pb2 import Timestamp

import chat_pb2
import chat_pb2_grpc


class Client:
    chat = []

    def __init__(self, name, ip, port):
        self.name = name

        # create a gRPC channel + stub
        channel = grpc.insecure_channel(ip + ':' + str(port))
        self.conn = chat_pb2_grpc.ChatStub(channel)
        # create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()

        # main loop
        while 1:
            text = input()
            if not Client.grpc_server_on(channel):
                break
            self.chat.append(text)
            msg = chat_pb2.Msg()
            msg.name = name
            msg.content = text
            msg.timestamp.GetCurrentTime()
            self.conn.C2S(msg)

    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        try:
            meta = chat_pb2.Meta()
            meta.name = self.name
            for msg in self.conn.S2C(meta):  # this line will wait for new messages from the server!
                line = f"[{msg.name}] at [{msg.timestamp.ToDatetime()}]: {msg.content}"
                print(line)  # debugging statement
                self.chat.append(line + '\n')  # add the message to the UI
        except: # TODO catch certain exception, not all of them
            print(f"Server disconnected. Press ENTER to exit (might take couple of sec)")

    @staticmethod
    def grpc_server_on(channel) -> bool:
        TIMEOUT_SEC = 5
        try:
            grpc.channel_ready_future(channel).result(timeout=TIMEOUT_SEC)
            return True
        except grpc.FutureTimeoutError:
            return False

if __name__ == '__main__':
    logging.basicConfig()
    c = Client()

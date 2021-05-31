# import socket library
import socket

# import threading library
import threading

# method for broadcasting
# messages to the each clients
def broadcastMessage(message):
    for client in clients:
        client.send(message)


# Lists that will contains
# all the clients connected to
# the server and their names.
clients, names = [], []


class Server:
    def __init__(self, server="127.0.0.1", port=5000, format_enc="utf-8"):
        # An IPv4 address is obtained
        # for the server.
        self.server_addr = server

        # Choose a port that is free
        self.PORT = port

        self.address = (server, port)

        self.format_enc = format_enc

        # Create a new socket for
        # the server
        self.server_socket = socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM)

        # bind the address of the
        # server to the socket
        self.server_socket.bind(self.address)

    # function to start the connection
    def startChat(self):
        print("server is working on " + self.server_addr)

        # listening for connections
        self.server_socket.listen()

        while True:
            # accept connections and returns
            # a new connection to the client
            #  and  the address bound to it
            conn, addr = self.server_socket.accept()
            conn.send("NAME".encode(self.format_enc))

            # 1024 represents the max amount
            # of data that can be received (bytes)
            name = conn.recv(1024).decode(self.format_enc)

            # append the name and client
            # to the respective list
            names.append(name)
            clients.append(conn)

            print(f"Name is :{name}")

            # broadcast message
            broadcastMessage(f"{name} has joined the chat!".encode(self.format_enc))

            conn.send('Connection successful!'.encode(self.format_enc))

            # Start the handling thread
            thread = threading.Thread(target=self.handle,
                                      args=(conn, addr))
            thread.start()

            # no. of clients connected
            # to the server
            print(f"active connections {threading.activeCount() - 1}")


    # method to handle the
    # incoming messages
    def handle(self, conn, addr):
        print(f"new connection {addr}")
        connected = True

        while connected:
            # recieve message
            message = conn.recv(1024)

            # broadcast message
            broadcastMessage(message)

        # close the connection
        conn.close()


if __name__ == '__main__':
    # call the method to
    # begin the communication
    server = Server()
    server.startChat()


# # Client
# from typing import List

# Msg = str

# chat: List[Msg] = []



# # Server
# chat: List[Msg] = []
# lchat: int

# def handleMsg() -> Msg:
#     new_msg = True
#     pass

# def gen():

#     if len(chat) - lchat > 0:
#         for msg in chat[lchat:]:
#             yield msg
#         lchat = len(chat)
from src.client import Client
from src.server import Server
from src.client_new import GUIClient
from src.server_new import GUIServer
from src.GUILogin import GUILogin

if __name__ == '__main__':
    #name = input("Enter your name - ")
    #role = input("Enter your role: S for server, C for client - ")
    login = GUILogin()

    if login.name == "" or login.role == "":
        exit()

    if (login.role == 'S'):
        #name = input("Enter your name - ")
        s = GUIServer(login.name)
    elif (login.role == 'C'):
        #ip = input("Enter Server IP")
        #port = input("Enter Server Port")

        import socket
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        port = 50051

        c = GUIClient(login.name, ip, port)
    else:
        print(f"Incorrect role {login.role}")

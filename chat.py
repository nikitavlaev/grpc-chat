from src.client import Client
from src.server import Server


if __name__ == '__main__':
    name = input("Enter your name - ")
    role = input("Enter your role: S for server, C for client - ")

    if (role == 'S'):
        s = Server(name)
    elif (role == 'C'):
        # ip = input("Enter Server IP")
        # port = input("Enter Server Port")
        
        # DEBUG
        import socket
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        port = 50051
        # END DEBUG

        c = Client(name, ip, port)
    else:
        print(f"Incorrect role {role}")
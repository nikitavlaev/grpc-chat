from argparse import ArgumentParser
import logging
import sys

from src.client import GUIClient
from src.server import GUIServer
from src.GUILogin import GUILogin

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-v',
        '--verbose',
        dest='v',
        help='Output logs to console',
        action = 'store_true'
    )
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.v:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        root.addHandler(handler)

    login = GUILogin()
    if login.name == "" or login.role == "":
        exit()

    if (login.role == 'S'):
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
        logging.critical(f"Incorrect role: {login.role}")

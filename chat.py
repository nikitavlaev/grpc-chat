from argparse import ArgumentParser
import logging
import sys

from src.client import Client
from src.server import Server
from src.login import Login
from src.connection_info_retriever import ConnectionInfoRetriever

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

    login = Login()
    if login.name == "" or login.role == "":
        exit()

    if (login.role == 'S'):
        s = Server(login.name)
    elif (login.role == 'C'):
        cir = ConnectionInfoRetriever()
        if cir.premature_exit:
            exit()
        else:
            c = Client(login.name, cir.ip, cir.port)
    else:
        logging.critical(f"Incorrect role: {login.role}")

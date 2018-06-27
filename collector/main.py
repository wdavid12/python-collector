import socketserver
import argparse, sys, time
import select
import socket
from io import BytesIO

import ipfix.ie

from .processor import flow_processor
from .constants import *


def parse_args():
    parser = argparse.ArgumentParser(description="Display IPFIX flows")
    parser.add_argument('--bind', '-b', metavar="bind", nargs="?",
                        default="127.0.0.1", help="address to bind to as Collector (default all)")
    parser.add_argument('--port', '-p', metavar="port", nargs="?", type=int,
                        default="4739", help="port to bind to as Collector (default 4739)")
    return parser.parse_args()

def main_loop(sock):
    flow_processor.draw_screen()
    while True:
        r,w,e = select.select([sock], [], [], TIMEOUT)
        if sock in r:
            data, _ = sock.recvfrom(MTU)
            flow_processor.process_data(data)
        flow_processor.draw_screen()

if __name__ == "__main__":

    # get args
    args = parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.bind, args.port))

    try:
        main_loop(sock)
    except KeyboardInterrupt:
        sys.exit('\nCtrl-C caught. Exiting.')

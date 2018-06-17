import socketserver
import argparse, sys, time
from threading import Thread

import ipfix.ie

from .processor import flow_processor
from .constants import *


def parse_args():
    parser = argparse.ArgumentParser(description="Display IPFIX flows")
    parser.add_argument('--bind', '-b', metavar="bind", nargs="?",
                        default="", help="address to bind to as Collector (default all)")
    parser.add_argument('--port', '-p', metavar="port", nargs="?", type=int,
                        default="4739", help="port to bind to as Collector (default 4739)")
    return parser.parse_args()


class UdpIPFIXHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        flow_processor.process_data(self.rfile)


def update_display():
    while True:
        flow_processor.draw_screen()
        time.sleep(5)


if __name__ == "__main__":

    # get args
    args = parse_args()

    flow_processor.draw_screen()

    t = Thread(target=update_display, daemon=True)
    t.start()

    ss = socketserver.UDPServer((args.bind, args.port), UdpIPFIXHandler)

    try:
        ss.serve_forever()
    except KeyboardInterrupt:
        sys.exit('\nCtrl-C caught. Exiting.')

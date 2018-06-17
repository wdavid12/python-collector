import socket
import argparse
import time
import random
import sys
from ipaddress import ip_address

import ipfix.message

from .constants import *
from .sampling_template import *

def parse_args():
    parser = argparse.ArgumentParser(description="Send dummy IPFIX traffic.")
    parser.add_argument('--target', '-t', metavar="target", nargs="?",
                        default="127.0.0.1", help="address to send traffic to")
    parser.add_argument('--port', '-p', metavar="port", nargs="?", type=int,
                        default="4739", help="port to send traffic to")
    return parser.parse_args()


def gen_test_msgs(socket, args, tmpl, count=4):
    elements = {
            "sourceMacAddress": b"\xff"*6,
            "destinationMacAddress": b"\xff"*6,
            "sourceIPv4Address": ip_address(0x7f000000+1),
            "destinationIPv4Address": ip_address(0x7f000000+2),
            "protocolIdentifier": 17,
    }

    m = ipfix.message.MessageBuffer()
    m.begin_export(odid=OBS_DOMAIN_ID)
    m.add_template(tmpl, export=False)
    loop_count = 0

    while True:
        m.begin_export(odid=OBS_DOMAIN_ID)
        m.export_ensure_set(SAMPLING_SET_ID)
        for _ in range(count):
            elements["sourceTransportPort"] = random.choice([123,456])
            elements["destinationTransportPort"] = random.choice([1111,2222])
            m.export_namedict(elements)

        s.sendto(m.to_bytes(), (args.target, args.port))
        loop_count += 1

        if loop_count % 100 == 0:
            sys.stderr.write('.')
            sys.stderr.flush()
            loop_count = 0

        time.sleep(0.1)


if __name__ == "__main__":
    args = parse_args()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tmpl = build_sampling_template()
    gen_test_msgs(s, args, tmpl)




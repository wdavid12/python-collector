import ipfix.reader

import collections
import time

from threading import Lock

from .parser import Parser
from .sampling_template import *
from .constants import *


class FlowCounter():
    def __init__(self):
        self.total_count = 0
        self.count = 0
        # self.prev_rate = 0

    def inc(self):
        self.count += 1
        self.total_count += 1

    def reset(self):
        self.count = 0


class FlowProcessor():
    def __init__(self):
        self.flows = collections.OrderedDict()
        self.start_time = time.time()
        self.prev_time = time.time()
        self.template = build_sampling_template()


    def draw_screen(self, debug=False):
        now = time.time()
        total_elapsed = int(now - self.start_time)
        count_time = now - self.prev_time

        if count_time < 1:
            return

        print(CLEAR_STR)

        if debug:
            self.debug_print()

        self.prev_time = now

        print('[ %s ][ Elapsed: %-10d seconds ][ %s ]\n' % (
            'IPFIX Flows', total_elapsed, time.ctime(now)))

        print("%-45s %-25s %s\n" % ('Flow','Rate (packets/sec)','Total Count'))

        for k,v in self.flows.items():
            rate = v.count / count_time
            # rate = (v.prev_rate * ALPHA) + (rate * (1-ALPHA))
            # v.prev_rate = rate
            print("%-45s %-25f %d" % (k, rate, v.total_count))
            v.reset()


    def debug_print(self):
        print('number of entries: %d' % len(self.flows))


    def format_record(self, rec):
        key = []
        transport = False
        proto = rec["protocolIdentifier"]
        if proto in [6,17]:
            transport = True

        if proto in PROTOCOLS:
            key.append(PROTOCOLS[proto])
        else:
            key.append('unknown: ')
        key.append(str(rec["sourceIPv4Address"]))
        if transport:
            key.append(":"+str(rec["sourceTransportPort"]))

        key.append(' => ')
        key.append(str(rec["destinationIPv4Address"]))
        if transport:
            key.append(":"+str(rec["destinationTransportPort"]))

        return ''.join(key)


    def process_data(self, buff):

        r = Parser(self.template, buff)
        r.parse()

        for rec in r.namedict_iterator():
            key = self.format_record(rec)
            if key not in self.flows:
                self.flows[key] = FlowCounter()
            self.flows[key].inc()


flow_processor = FlowProcessor()

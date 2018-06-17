import ipfix.reader

import collections
import time

from threading import Lock

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


class ReaderWithTemplate(ipfix.reader.MessageStreamReader):
    def __init__(self, stream, template):
        super().__init__(stream)
        self.msg.odid = OBS_DOMAIN_ID
        self.msg.add_template(template, export=False)
        self.msg.accepted_tids.add((OBS_DOMAIN_ID, template.tid))


class FlowProcessor():
    def __init__(self):
        self.flows = collections.OrderedDict()
        self.start_time = time.time()
        self.prev_time = time.time()
        self.template = build_sampling_template()
        self.mutex = Lock()


    def draw_screen(self):
        with self.mutex:
            print(CLEAR_STR)

            now = time.time()
            total_elapsed = int(now - self.start_time)
            count_time = now - self.prev_time
            self.prev_time = now

            print('[ %s ][ Elapsed: %-10d seconds ][ %s ]\n' % (
                'IPFIX Flows', total_elapsed, time.ctime(now)))

            print("%-40s %-25s %s\n" % ('Flow','Rate (packets/sec)','Total Count'))

            for k,v in self.flows.items():
                rate = v.count / count_time
                # rate = (v.prev_rate * ALPHA) + (rate * (1-ALPHA))
                # v.prev_rate = rate
                print("%-40s %-25f %d" % (k, rate, v.total_count))
                v.reset()


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


    def process_data(self, instream):

        r = ReaderWithTemplate(instream, self.template)

        with self.mutex:
            for rec in r.namedict_iterator():
                key = self.format_record(rec)
                if key not in self.flows:
                    self.flows[key] = FlowCounter()
                self.flows[key].inc()


flow_processor = FlowProcessor()

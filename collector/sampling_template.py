
import ipfix.ie
import ipfix.template

from .constants import *

def build_sampling_template():

    # initialize information model
    ipfix.ie.use_iana_default()
    ipfix.ie.use_5103_default()

    elements = ["sourceMacAddress",
                "destinationMacAddress",
                "sourceIPv4Address",
                "destinationIPv4Address",
                "protocolIdentifier",
                "sourceTransportPort",
                "destinationTransportPort"]

    tmpl = ipfix.template.from_ielist(SAMPLING_SET_ID,
            ipfix.ie.spec_list(elements))

    return tmpl


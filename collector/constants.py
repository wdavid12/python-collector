# Constants used in collector and exporter

# Set id of samples. Must be the same as in OVS sources
SAMPLING_SET_ID = 376

# Observation Domain ID. Must match the one in OVS exporter
# configuration.
OBS_DOMAIN_ID = 2

# IP protocols
PROTOCOLS = {
        6  : 'tcp: ',
        17 : 'udp: ',
        1  : 'icmp: '
}

# Collector refresh interval in seconds.
UPDATE_INTERVAL = 5

# Constants for printing
CLEAR_STR  = chr(27) + '[2J' + chr(27) + '[H'

# For smoothed rate calculation
ALPHA = 0.2

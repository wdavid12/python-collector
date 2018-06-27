import struct

from ipfix.template import IpfixDecodeError

_sethdr_st = struct.Struct("!HH")
_msghdr_st = struct.Struct("!HHLLL")


class Parser(object):
    """
    Implements an IPFIX parser for a specific template.

    """
    def __init__(self, tmpl, buff):
        self.mbuf = buff
        self.tmpl = tmpl
        self.setlist = []

    def parse(self):
        (version, length, export_epoch, sequence, odid) = \
                _msghdr_st.unpack_from(self.mbuf, 0)

        # verify version and length
        if version != 10:
            raise IpfixDecodeError("Illegal or unsupported version " +
                                       str(version))

        if length < 20 or length > len(self.mbuf):
            raise IpfixDecodeError("Illegal message lengths" +
                                       str(length) + " " + str(len(self.mbuf)))

        offset = _msghdr_st.size

        while offset < length:
            (setid, setlen) = _sethdr_st.unpack_from(self.mbuf, offset)
            if offset + setlen > length:
                raise IpfixDecodeError("Set too long for message")
            if setlen == 0:
                raise IpfixDecodeError("Set of length zero recieved")
            self.setlist.append((offset, setid, setlen))
            offset += setlen


    def namedict_iterator(self):
        for (offset, setid, setlen) in self.setlist:
            setend = offset + setlen
            offset += _sethdr_st.size # skip set header in decode
            if setid != self.tmpl.tid:
                continue
            while offset + self.tmpl.minlength <= setend:
                (rec, offset) = self.tmpl.decode_namedict_from(self.mbuf, offset)
                yield rec

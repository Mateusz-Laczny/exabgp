# encoding: utf-8
"""
prefix.py

Created by Thomas Mangin on 2022-04-27.
Copyright (c) 2022-2022 Exa Networks. All rights reserved.
License: 3-clause BSD. (See the COPYRIGHT file)
"""

#   https://www.rfc-editor.org/rfc/rfc7752.html#section-3.2.1.5

# The Multi-Topology ID (MT-ID) TLV carries one or more IS-IS or OSPF
# Multi-Topology IDs for a link, node, or prefix.

# Semantics of the IS-IS MT-ID are defined in Section 7.2 of RFC 5120
# [RFC5120].  Semantics of the OSPF MT-ID are defined in Section 3.7 of
# RFC 4915 [RFC4915].  If the value in the MT-ID TLV is derived from
# OSPF, then the upper 9 bits MUST be set to 0.  Bits R are reserved
# and SHOULD be set to 0 when originated and ignored on receipt.

# The format of the MT-ID TLV is shown in the following figure.

# 	0                   1                   2                   3
# 	0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# 	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# 	|              Type             |          Length=2*n           |
# 	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# 	|R R R R|  Multi-Topology ID 1  |             ....             //
# 	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# 	//             ....             |R R R R|  Multi-Topology ID n  |
# 	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# 				Figure 12: Multi-Topology ID TLV Format

# where Type is 263, Length is 2*n, and n is the number of MT-IDs
# carried in the TLV.

# The MT-ID TLV MAY be present in a Link Descriptor, a Prefix
# Descriptor, or the BGP-LS attribute of a Node NLRI.  In a Link or
# Prefix Descriptor, only a single MT-ID TLV containing the MT-ID of
# the topology where the link or the prefix is reachable is allowed.
# In case one wants to advertise multiple topologies for a given Link
# Descriptor or Prefix Descriptor, multiple NLRIs need to be generated
# where each NLRI contains an unique MT-ID.  In the BGP-LS attribute of
# a Node NLRI, one MT-ID TLV containing the array of MT-IDs of all
# topologies where the node is reachable is allowed.
# ================================================================== InterfaceAddress

import struct


class _Topology:
    def __init__(self, bits, tid):
        self.bits = bits
        self.tid = tid

    def json(self):
        return '{ "bits": "%s", "multi-topology-id": %d }' % (
            (('0000' + bin(self.bits)[2:])[-4:]),
            self.tid
        )


class MTID(object):
    def __init__(self, topologies, packed=None):
        self.topologies = topologies
        self._packed = packed

    @classmethod
    def unpack(cls, data):
        tids = []
        for i in range(0, len(data), 2):
            payload = struct.unpack('!H', data[i:i+2])[0]
            bits = payload >> (16-4)
            tid = payload & 0x0FFF
            tids.append(_Topology(bits, tid))
        return cls(tids, data)

    def json(self):
        tids = ', '.join(_.json() for _ in self.topologies)
        return f'[{tids}]'

    def __eq__(self, other):
        return self.topologies == other.topologies

    def __neq__(self, other):
        return self.topologies != other.topologies

    def __lt__(self, other):
        raise RuntimeError('Not implemented')

    def __le__(self, other):
        raise RuntimeError('Not implemented')

    def __gt__(self, other):
        raise RuntimeError('Not implemented')

    def __ge__(self, other):
        raise RuntimeError('Not implemented')

    def __str__(self):
        return ':'.join('%02X' % _ for _ in self.pack())

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self._packed)

    def __hash__(self):
        return hash(str(self))

    def pack(self):
        if self._packed:
            return self._packed
        raise RuntimeError('Not implemented')

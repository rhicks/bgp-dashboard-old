#! /usr/bin/env python3
from reader import FileReaderIPv4
from autonomoussystem import AutonomousSystem
from ipv4prefix import IPv4Prefix
from datetime import datetime
import sys
import socket
import subprocess


class Manager(object):
    """Program manager"""

    def __init__(self):
        self.filename = FileReaderIPv4("../../bgp-data-full.txt")
        self.data = self.filename.get_data()
        self.default_asn = "3701"


def get_data():
    manager = Manager()
    print("Processing data:", end="")
    start_time = datetime.now()
    for line in manager.data:
        if IPv4Prefix.get_count() % 10000 == 0:
            print(".", end="")
            sys.stdout.flush()
        status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin = line
        Route = IPv4Prefix(status, prefix, next_hop_ip, metric,
                           local_pref, weight, as_path, origin, manager.default_asn)
        if Route.destination_asn in AutonomousSystem.dict_of_all:
            old_asn = AutonomousSystem.dict_of_all.get(Route.destination_asn)
            old_asn.add_ipv4_prefix(Route)
        else:
            new_asn = AutonomousSystem(Route.destination_asn)
            new_asn.add_ipv4_prefix(Route)

    print()
    print("Processing Time: " + str(datetime.now() - start_time))
    print("IPv4 Routing Table Size:", IPv4Prefix.get_count())
    print("Unique ASNs:", len(AutonomousSystem.dict_of_all))

    next_hops = []

    for k, v in AutonomousSystem.dict_of_all.items():
        for route in v.get_ipv4_prefixes():
            next_hops.append(route.next_hop_asn)

    peers = (set(next_hops))


    for peer in peers:
        if (peer and (int(peer) < 64512 or int(peer) > 65534)) :
            # print(peer)
            # print(subprocess.getoutput("whois -h whois.cymru.com \" -n -f AS\"" + peer))
            print(peer, subprocess.getoutput("dig +short AS" + peer + ".asn.cymru.com TXT").split("|")[-1])
        else:
            pass

    print()
    print("Processing Time: " + str(datetime.now() - start_time))
    print("IPv4 Routing Table Size:", IPv4Prefix.get_count())
    print("Unique ASNs:", len(AutonomousSystem.dict_of_all))
    print("Peer Networks:", len(peers))


if __name__ == '__main__':
    get_data()

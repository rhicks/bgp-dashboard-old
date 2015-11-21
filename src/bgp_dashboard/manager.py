#! /usr/bin/env python3
from reader import FileReaderIPv4
from autonomoussystem import AutonomousSystem
from ipv4prefix import IPv4Prefix


class Manager(object):
    """Program manager"""

    def __init__(self):
        self.filename = FileReaderIPv4("../../bgp-data-full.txt")
        self.data = self.filename.get_data()
        self.default_asn = "3701"


def get_data():
    manager = Manager()
    for line in manager.data:

        status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin = line
        Route = IPv4Prefix(status, prefix, next_hop_ip, metric,
                           local_pref, weight, as_path, origin, manager.default_asn)
        if Route.destination_asn in AutonomousSystem.dict_of_all:
            old_asn = AutonomousSystem.dict_of_all.get(Route.destination_asn)
            old_asn.add_ipv4_prefix(Route)
        else:
            new_asn = AutonomousSystem(Route.destination_asn)
            new_asn.add_ipv4_prefix(Route)

    print("IPv4 Routing Table Size:", IPv4Prefix.get_count())
    print("Unique ASNs:", len(AutonomousSystem.dict_of_all))

    myASN = AutonomousSystem.dict_of_all.get("6509")
    for route in myASN.get_ipv4_prefixes():
        print(route.next_hop_asn)


if __name__ == '__main__':
    get_data()

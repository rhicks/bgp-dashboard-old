#! /usr/bin/env python3
from reader import FileReaderIPv4
from autonomoussystem import AutonomousSystem
from collections import defaultdict


class Manager:
    """Program manager"""

    def __init__(self):
        self.filename = FileReaderIPv4("../../bgp-data-full.txt")
        self.data = self.filename.get_data()
        self.default_asn = "3701"


class Autonomous_System:
    list_of_all = {}

    def __init__(self, as_number):
        self.list_of_ipv4_prefixes = []
        self.as_number = as_number
        # Autonomous_System.list_of_all.add(self)
        Autonomous_System.list_of_all[self.as_number] = self

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # def __hash__(self):
    #     return hash(self.as_number)

    def add_prefix(self, ipv4_prefix):
        self.list_of_ipv4_prefixes.append(ipv4_prefix)
        # print("Appended %d to %d", ipv4_prefix.prefix, self.as_number)


class IPv4_Prefix:
    count = 0

    def __init__(self, status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin, manager):
        IPv4_Prefix.count = IPv4_Prefix.count + 1
        self.status = status
        self.prefix = prefix
        self.next_hop_ip = next_hop_ip
        self.metric = metric
        self.local_pref = local_pref
        self.weight = weight
        self.as_path = as_path
        self.origin = origin
        if self.as_path:
            self.next_hop_asn = self.as_path[0]
            if "{" in self.as_path[-1]:
                self.destination_asn = self.as_path[-2]
            else:
                self.destination_asn = self.as_path[-1]
        else:
            self.next_hop_asn = None
            self.destination_asn = manager.default_asn

    def __str__(self):
        return str(self.__dict__)

    @staticmethod
    def get_count():
        return IPv4_Prefix.count


def get_data():
    manager = Manager()
    for line in manager.data:
        # create the route objects
        status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin = line
        Route = IPv4_Prefix(status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin, manager)
        if Route.destination_asn in Autonomous_System.list_of_all:
            old_asn = Autonomous_System.list_of_all.get(Route.destination_asn)
            old_asn.add_prefix(Route)
        else:
            new_asn = Autonomous_System(Route.destination_asn)
            new_asn.add_prefix(Route)

    print("IPv4 Routing Table Size:", IPv4_Prefix.get_count())
    print("Unique ASNs:", len(Autonomous_System.list_of_all))

    myASN = Autonomous_System.list_of_all.get("25899")
    for route in myASN.list_of_ipv4_prefixes:
        print(route)


if __name__ == '__main__':
    get_data()

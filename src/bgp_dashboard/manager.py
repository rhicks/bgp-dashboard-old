#! /usr/bin/env python3
from reader import FileReaderIPv4
from autonomoussystem import AutonomousSystem
from collections import defaultdict

# get the data
# read the route line
# if the AS doesn't exist
#   then create it
# else
#   Add the IPv4 prefix to the AS object with the full AS_PATH
#

class Manager:
    """Program manager"""
    def __init__(self):
        self.filename = FileReaderIPv4("../../bgp-data-full.txt")
        self.data = self.filename.get_data()
        self.default_asn = "3701"

class Autonomous_System:
    dict_of_Autonomous_Systems = {}
    def __init__(self, as_number):
        self.list_of_ipv4_prefixes = []
        self.as_number = as_number
        Autonomous_System.dict_of_Autonomous_Systems[self.as_number] = self

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

    @staticmethod
    def get_count():
        return IPv4_Prefix.count



def get_data():
    manager = Manager()
    for line in manager.data:
        # create the route objects
        status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin = line
        Route = IPv4_Prefix(status, prefix, next_hop_ip, metric,  local_pref, weight, as_path, origin, manager)
        # add the route objects to the parent ASN list of routes
        if Route.destination_asn not in Autonomous_System.dict_of_Autonomous_Systems:
            new_asn = Autonomous_System(Route.destination_asn)
            new_asn.list_of_ipv4_prefixes.append(Route)
        else:
            Autonomous_System.dict_of_Autonomous_Systems[Rout.destination_asn].list_of_ipv4_prefixes
            pass
    print("IPv4 Routing Table Size:", IPv4_Prefix.get_count())
    print("Unique ASNs:", len(Autonomous_System.dict_of_Autonomous_Systems))



if __name__ == '__main__':
    get_data()

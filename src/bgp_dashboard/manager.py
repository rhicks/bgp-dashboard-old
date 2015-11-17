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
        self.asn_set = set()

class ASN:
    as_dict = {}
    def __init__(self, as_number):
        self.list_of_ipv4_prefixes = []
        self.as_number = as_number
        ASN.as_dict[self.as_number] = self

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
        status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin = line
        Route = IPv4_Prefix(status, prefix, next_hop_ip, metric,  local_pref, weight, as_path, origin, manager)
        if Route.destination_asn not in ASN.as_dict:
            myASN = ASN(Route.destination_asn)
            myASN.list_of_ipv4_prefixes.append(Route)
        else:
            pass

    for asn in ASN.as_dict:
        print(asn)
        # for network in value.list_of_ipv4_prefixes:
        #     print(key, network)
    # print(myASN.list_of_ipv4_prefixes)
        # manager.asn_set.add(myASN)
    # for key, value in ASN.as_dict.items():
    #     print(key)
    print("IPv4 Routing Table Size:", IPv4_Prefix.get_count())
    print("Unique ASNs:", len(ASN.as_dict))
    # print(ASN.as_dict)
    # for asn in manager.asn_set:
    #     print(asn.as_number)
    #

        # print(Route.next_hop_asn)
        # print(Route.destination_asn)

    #     if line[6]:
    #         asn = int(line[6][0])
    #         manager.asn_list[asn] = AutonomousSystem(asn)
    #     else:
    #         asn = int(manager.default_asn)
    #         manager.asn_list[asn] = AutonomousSystem(asn)
    # for myASN in manager.asn_list:
    #     print(myASN)
    # print(manager.asn_list)



if __name__ == '__main__':
    get_data()


# ASN
#     as_number = 3701
#     list_of_ipv4_prefixes = list
#
# IPv4_Prefix
#     prefix = 1.0.0.0/24
#     next_hop_ip = 198.32.195.34
#     metric = 0
#     local_pref = 1000
#     weight = 0
#     as_path = 15169
#     origin = i

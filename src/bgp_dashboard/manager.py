
from reader import FileReader
from autonomoussystem import AutonomousSystem
from prefix import Prefix
from collections import OrderedDict
from collections import Counter
import sys
import subprocess
import json
import socket
import dns.resolver
import re

DEFAULT_ASN = '3701'
# DEFAULT_FILENAME = 'bgp-data.txt'


class Manager(object):
    '''Program manager'''

    def __init__(self, filename):
        self.filename = FileReader(filename)

    def build_autonomous_systems(self):
        print('Processing data:', end='')
        data = self.filename.get_data()
        for line in data:
            if Prefix.get_count() % 10000 == 0:
                print('.', end='')
            sys.stdout.flush()
            prefix = self.create_prefix(line)
            asn = prefix.origin_asn
            next_hop = prefix.next_hop_asn
            if asn not in AutonomousSystem.dict_of_all:
                self.create_new_asn(asn).ipv4_prefixes.append(prefix)
            else:
                self.find_asn(asn).ipv4_prefixes.append(prefix)
            if next_hop:
                if next_hop not in AutonomousSystem.dict_of_all:
                    self.create_new_asn(next_hop).ipv4_next_hop_prefixes.append(prefix)
                else:
                    self.find_asn(next_hop).ipv4_next_hop_prefixes.append(prefix)
            else:
                pass

    def create_new_asn(self, asn):
        return AutonomousSystem(asn)

    def find_asn(self, asn):
        return AutonomousSystem.dict_of_all.get(asn)

    def create_prefix(self, line):
        return Prefix(*line)

    def list_of_peers(self):
        next_hops = []
        for k, v in AutonomousSystem.dict_of_all.items():
            for route in v.ipv4_prefixes:
                next_hops.append(route.next_hop_asn)
        return set(next_hops)

    def find_prefixes(self, asn):
        prefixes = self.find_asn(asn).ipv4_prefixes
        count = len(prefixes)
        return prefixes, count

    def _sorted_ip_list(self, ip_list):
        mylist = list()
        for line in ip_list:
            mylist.append(line.prefix)
        return(mylist)
        #return sorted(list({line.prefix for line in ip_list}), key=lambda x: socket.inet_aton(x.split("/")[0]))


    def find_next_hop_prefixes(self, asn):
        prefixes = self.find_asn(asn).ipv4_next_hop_prefixes
        count = len(prefixes)
        return prefixes, count

    def _next_hop_asns(self, asn):
        next_hops = []
        for prefix in self.find_prefixes(asn)[0]:
            next_hops.append(prefix.next_hop_asn)
        return list(set(next_hops))

    def _next_hop_ips(self, prefix_list):
        next_hop_ips = []
        for prefix in prefix_list:
            next_hop_ips.append(prefix.next_hop_ip)
        c = Counter(next_hop_ips)
        return c, len(c)

    def _dns_query(self, asn):
        query = 'AS' + asn + '.asn.cymru.com'
        answers = dns.resolver.query(query, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                return txt_string.split('|')[-1].split(",", 2)[0].strip()

    def print_stats(self):
        print()
        print('IPv4 Routing Table Size:', Prefix.get_count())
        print('Unique ASNs:', len(AutonomousSystem.dict_of_all))
        print('Peer Networks:', len(self.list_of_peers()))

    def print_details(self):
        results = OrderedDict()
        results['peers'] = OrderedDict()
        print()
        for peer in sorted(list(filter(None.__ne__, self.list_of_peers())), key=lambda x: int(x)):
            if (peer and (int(peer) < 64512 or int(peer) > 65534)):
                results['peers'][peer] = OrderedDict()
                results['peers'][peer]['name'] = self._dns_query(peer)
                results['peers'][peer]['prefixes originated'] = self.find_prefixes(peer)[1]
                results['peers'][peer]['routes selected'] = self.find_next_hop_prefixes(peer)[1]
                all_next_hop_prefixes, count_next_hop_prefixes = self.find_next_hop_prefixes(peer)
                results['peers'][peer]['peering connections'] = self._next_hop_ips(all_next_hop_prefixes)[1]
                results['peers'][peer]['peering connection ip list route count'] = self._next_hop_ips(all_next_hop_prefixes)[0]
            else:
                pass
        print(json.dumps(results, indent=4))

    def print_asn_details(self, asn, show_routes):
        if self.find_asn(asn):
            results = OrderedDict()
            print()
            if asn in self.list_of_peers():
                name = self._dns_query(asn)
                results['asn'] = asn
                results['name'] = name
                results['peer'] = True
                prefixes, count = self.find_prefixes(asn)
                all_next_hop_prefixes, count_next_hop_prefixes = self.find_next_hop_prefixes(asn)
                received_prefixes_peering = []
                received_prefixes_other = []
                results['prefixes originated'] = count
                for prefix in prefixes:
                    if prefix.as_path[0] == asn:
                        received_prefixes_peering.append(prefix)
                    else:
                        received_prefixes_other.append(prefix)
                results['peering connections'] = self._next_hop_ips(all_next_hop_prefixes)[1]
                results['peering connection ip list route count'] = self._next_hop_ips(all_next_hop_prefixes)[0]
                results['prefixes originated by this asn that use the direct peering as a next hop'] = len(received_prefixes_peering)
                results['prefixes originated by this asn that do use the direct peering'] = len(received_prefixes_other)
                results['all prefixes using this asn as next hop'] = count_next_hop_prefixes
                if show_routes:
                    results['direct peering prefixes'] = self._sorted_ip_list(received_prefixes_peering)
                    results['non-peering prefixes'] = self._sorted_ip_list(received_prefixes_other)
                    results['all prefixes using this asn as transit'] = self._sorted_ip_list(all_next_hop_prefixes)
                results['next hop asn list'] = self._next_hop_asns(asn)
                print(json.dumps(results, indent=4))
            else:
                name = self._dns_query(asn)
                results['asn'] = asn
                results['name'] = name
                results['peer'] = False
                prefixes, count = self.find_prefixes(asn)
                received_prefixes_other = []
                results['prefixes originated'] = count
                for prefix in prefixes:
                    received_prefixes_other.append(prefix)
                if show_routes:
                    results['prefix list'] = self._sorted_ip_list(received_prefixes_other)
                results['next hop asn list'] = self._next_hop_asns(asn)
                print(json.dumps(results, indent=4))
        else:
            print()
            print("ASN %s not found" % asn)
            print("Ignored Lines:")
            for line in self.filename.get_ignored_lines():
                print(line)

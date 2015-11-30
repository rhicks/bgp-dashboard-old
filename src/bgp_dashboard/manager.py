
from reader import FileReaderIPv4
from autonomoussystem import AutonomousSystem
from ipv4prefix import IPv4Prefix
from collections import OrderedDict
import sys
import subprocess
import json
import socket

DEFAULT_ASN = '3701'
# DEFAULT_FILENAME = 'bgp-data.txt'


class Manager(object):
    '''Program manager'''

    def __init__(self, filename):
        self.filename = FileReaderIPv4(filename)

    def build_autonomous_systems(self):
        print('Processing data:', end='')
        data = self.filename.get_data()
        for line in data:
            if IPv4Prefix.get_count() % 10000 == 0:
                print('.', end='')
                sys.stdout.flush()
            prefix = self.create_prefix(line)
            asn = prefix.destination_asn
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
                # these are "local" asn next hops. do something with them.
                pass

    def create_new_asn(self, asn):
        return AutonomousSystem(asn)

    def find_asn(self, asn):
        return AutonomousSystem.dict_of_all.get(asn)

    def create_prefix(self, line):
        return IPv4Prefix(*line, default_asn=DEFAULT_ASN)

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
        return sorted(list({line.prefix for line in ip_list}),
                      key=lambda x: socket.inet_aton(x.split("/")[0]))

    def find_next_hop_prefixes(self, asn):
        prefixes = self.find_asn(asn).ipv4_next_hop_prefixes
        count = len(prefixes)
        return prefixes, count

    def _dns_query(self, asn):
        # migrate away from a system call
        query = 'dig +short AS' + asn + '.asn.cymru.com TXT'
        return subprocess.getoutput(query).split('|')[-1].split(",", 2)[0].strip()

    def print_details(self):
        results = OrderedDict()
        results['peers'] = OrderedDict()
        print()
        for peer in sorted(list(filter(None.__ne__, self.list_of_peers())), key=lambda x: int(x)):
            if (peer and (int(peer) < 64512 or int(peer) > 65534)):
                results['peers'][peer] = OrderedDict()
                results['peers'][peer]['name'] = self._dns_query(peer)
                results['peers'][peer]['prefixes originated'] = self.find_prefixes(peer)[1]
                results['peers'][peer]['prefixes advertised'] = self.find_next_hop_prefixes(peer)[1]
            else:
                pass
        print(json.dumps(results, indent=4))
        print()
        # move this to a --stats specific arg
        print('IPv4 Routing Table Size:', IPv4Prefix.get_count())
        print('Unique ASNs:', len(AutonomousSystem.dict_of_all))
        print('Peer Networks:', len(self.list_of_peers()))

    def print_asn_details(self, asn):
        results = {}
        print()
        if asn in self.list_of_peers():
            name = self._dns_query(asn)
            results['asn'] = asn
            results['name'] = name
            results['peer'] = True
            prefixes, count = self.find_prefixes(asn)
            received_prefixes_peering = []
            received_prefixes_other = []
            results['prefix count originated'] = count
            for prefix in prefixes:
                if prefix.as_path[0] == asn:
                    received_prefixes_peering.append(prefix)
                else:
                    received_prefixes_other.append(prefix)
            results['prefix count received peering'] = len(received_prefixes_peering)
            results['prefix count received other'] = len(received_prefixes_other)
            results['prefixes peering'] = self._sorted_ip_list(received_prefixes_peering)
            results['prefixes other'] = self._sorted_ip_list(received_prefixes_other)
            print(json.dumps(results, indent=4, sort_keys=True))
        else:
            name = self._dns_query(asn)
            results['asn'] = asn
            results['name'] = name
            results['peer'] = False
            prefixes, count = self.find_prefixes(asn)
            received_prefixes_other = []
            results['prefix count originated'] = count
            for prefix in prefixes:
                received_prefixes_other.append(prefix)
            results['prefix count received other'] = len(received_prefixes_other)
            results['prefixes other'] = self._sorted_ip_list(received_prefixes_other)
            print(json.dumps(results, indent=4, sort_keys=True))

#! /usr/bin/env python3

"""BGP Dashboard CLI Interface

Usage:
  bgp-dashboard.py <asn> -f <filename>
  bgp-dashboard.py --version

Options:
  -h --help     Show this screen.
  -f            File Name where "show ip bgp" data is located
  --peers       List of all directly connected BGP peers
  --version     Show version.


"""

from reader import FileReaderIPv4
from autonomoussystem import AutonomousSystem
from ipv4prefix import IPv4Prefix
from docopt import docopt
import sys
import subprocess

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
            if asn not in AutonomousSystem.dict_of_all:
                self.create_new_asn(asn).ipv4_prefixes.append(prefix)
            else:
                self.find_asn(asn).ipv4_prefixes.append(prefix)

    def create_new_asn(self, asn):
        return AutonomousSystem(asn)

    def find_asn(self, asn):
        return AutonomousSystem.dict_of_all.get(asn)

    def create_prefix(self, line):
        status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin = line
        return IPv4Prefix(status, prefix, next_hop_ip, metric, local_pref,
                          weight, as_path, origin, DEFAULT_ASN)

    def list_of_peers(self):
        next_hops = []
        for k, v in AutonomousSystem.dict_of_all.items():
            for route in v.ipv4_prefixes:
                next_hops.append(route.next_hop_asn)
        return set(next_hops)

    def print_details(self):
        print()
        for peer in self.list_of_peers():
            if (peer and (int(peer) < 64512 or int(peer) > 65534)):
                dns_query = 'dig +short AS' + peer + '.asn.cymru.com TXT'
                print(peer, subprocess.getoutput(dns_query).split('|')[-1])
            else:
                pass
        print()
        print('IPv4 Routing Table Size:', IPv4Prefix.get_count())
        print('Unique ASNs:', len(AutonomousSystem.dict_of_all))
        print('Peer Networks:', len(self.list_of_peers()))


def main(args):
    if args['<filename>']:
        try:
            filename = args['<filename>']
            manager = Manager(filename)
            manager.build_autonomous_systems()
            manager.print_details()
        except(FileNotFoundError):
            print("\nFile not found: {0}".format(filename), file=sys.stderr)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='BGP Dashboard  0.0.1')
    print(arguments)
    try:
        sys.exit(main(arguments))
    except(KeyboardInterrupt):
        print("\nExiting on user request.\n", file=sys.stderr)
        sys.exit(1)

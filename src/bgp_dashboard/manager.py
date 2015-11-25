#! /usr/bin/env python3

"""BGP Dashboard CLI Interface

Usage:
  manager.py -f <filename>
  manager.py --version

Options:
  -h --help     Show this screen.
  -f            File Name where "show ip bgp" data is located
  --version     Show version.


"""

from reader import FileReaderIPv4
from autonomoussystem import AutonomousSystem
from ipv4prefix import IPv4Prefix
from docopt import docopt
import sys
import subprocess

DEFAULT_ASN = '3701'


class Manager(object):
    '''Program manager'''

    def __init__(self, filename):
        # self.filename = FileReaderIPv4('../../bgp-data-full-asr9k.txt')
        self.filename = FileReaderIPv4(filename)
        self.data = self.filename.get_data()
        # self.default_asn = DEFAULT_ASN

    def build_autonomous_systems(self):
        print('Processing data:', end='')
        for line in self.data:
            if IPv4Prefix.get_count() % 10000 == 0:
                print('.', end='')
                sys.stdout.flush()
            status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin = line
            Route = IPv4Prefix(status, prefix, next_hop_ip, metric,
                               local_pref, weight, as_path, origin, DEFAULT_ASN)
            if Route.destination_asn in AutonomousSystem.dict_of_all:
                old_asn = AutonomousSystem.dict_of_all.get(
                    Route.destination_asn)
                old_asn.ipv4_prefixes.append(Route)
            else:
                new_asn = AutonomousSystem(Route.destination_asn)
                new_asn.ipv4_prefixes.append(Route)

    def _list_of_peers(self):
        next_hops = []
        for k, v in AutonomousSystem.dict_of_all.items():
            for route in v.ipv4_prefixes:
                next_hops.append(route.next_hop_asn)
        return set(next_hops)

    def print_details(self):
        print()
        for peer in self._list_of_peers():
            if (peer and (int(peer) < 64512 or int(peer) > 65534)):
                print(peer, subprocess.getoutput('dig +short AS' + peer + '.asn.cymru.com TXT').split('|')[-1])
            else:
                pass
        print()
        print('IPv4 Routing Table Size:', IPv4Prefix.get_count())
        print('Unique ASNs:', len(AutonomousSystem.dict_of_all))
        print('Peer Networks:', len(self._list_of_peers()))


def get_data(filename):
    manager = Manager(filename)
    manager.build_autonomous_systems()
    manager.print_details()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='BGP Dashboard  0.0.1')
    try:
        sys.exit(get_data(arguments['<filename>']))
    except(KeyboardInterrupt):
        print("\nExiting on user request.\n", file=sys.stderr)
        sys.exit(1)

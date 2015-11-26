#! /usr/bin/env python3

"""BGP Dashboard CLI Interface

Usage:
  manager.py <asn> -f <filename>
  manager.py --version

Options:
  -h --help     Show this screen.
  -f            File Name where "show ip bgp" data is located
  --peers       List of all directly connected BGP peers
  --version     Show version.


"""

from reader import FileReaderIPv4
from autonomoussystem import AutonomousSystem
# from ipv4prefix import IPv4Prefix
from docopt import docopt
import sys
import subprocess
from collections import namedtuple

DEFAULT_ASN = '3701'
# DEFAULT_FILENAME = 'bgp-data.txt'


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
            prefix = self._create_prefix(line)
            # print(prefix)
            # if len(AutonomousSystem.dict_of_all) % 10000 == 0:
            #     print('.', end='')
            #     sys.stdout.flush()
            # if IPv4Prefix.get_count() % 10000 == 0:
            #     print('.', end='')
            #     sys.stdout.flush()
            # status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin = line
            # Route = IPv4Prefix(status, prefix, next_hop_ip, metric,
            #                    local_pref, weight, as_path, origin, DEFAULT_ASN)
            if prefix.destination_asn in AutonomousSystem.dict_of_all:
                old_asn = AutonomousSystem.dict_of_all.get(prefix.destination_asn)
                old_asn.ipv4_prefixes.append(prefix)
            else:
                new_asn = AutonomousSystem(prefix.destination_asn)
                new_asn.ipv4_prefixes.append(prefix)

    def _create_prefix(self, line):
        Prefix = namedtuple('Prefix', ['status', 'prefix', 'next_hop_ip', 'metric', 'local_pref', 'weight', 'as_path', 'origin', 'next_hop_asn', 'destination_asn'])
        status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin = line

        if as_path:
            next_hop_asn = as_path[0]
            if '{' in as_path[-1]:
                destination_asn = as_path[-2]
            else:
                destination_asn = as_path[-1]
        else:
            next_hop_asn = None
            destination_asn = DEFAULT_ASN

        return Prefix(status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin, next_hop_asn, destination_asn)





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
        # print('IPv4 Routing Table Size:', IPv4Prefix.get_count())
        print('Unique ASNs:', len(AutonomousSystem.dict_of_all))
        print('Peer Networks:', len(self._list_of_peers()))


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

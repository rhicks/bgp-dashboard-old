#! /usr/bin/env python3

"""BGP Dashboard CLI Interface

Usage:
  bgp-dashboard.py -f <filename> --asn <asn> [--routes]
  bgp-dashboard.py -f <filename> --peers [--routes]
  bgp-dashboard.py -f <filename> --stats
  bgp-dashboard.py --version

Options:
  -h --help     Show this screen.
  -f            File Name where "show ip bgp" data is located
  --asn         Get ASN details
  --peers       List of all directly connected BGP peers
  --routes      Show optional route details
  --stats       BGP routing stats
  --version     Show version.


"""

from manager import Manager
from docopt import docopt
import sys


def main(args):
    if args['<filename>']:
        try:
            filename = args['<filename>']
            manager = Manager(filename)
            manager.build_autonomous_systems()
            if args['<asn>']:
                asn = args['<asn>']
                show_routes = args['--routes']
                manager.print_asn_details(asn, show_routes)
            elif args['--peers']:
                show_routes = args['--routes']
                manager.print_details(show_routes)
            elif args['--stats']:
                manager.print_stats()
        except(FileNotFoundError):
            print("\nFile not found: {0}".format(filename), file=sys.stderr)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='BGP Dashboard  0.0.1')
    # print(arguments)
    try:
        sys.exit(main(arguments))
    except(KeyboardInterrupt):
        print("\nExiting on user request.\n", file=sys.stderr)
        sys.exit(1)

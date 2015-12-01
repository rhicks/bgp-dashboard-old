#! /usr/bin/env python3

"""BGP Dashboard CLI Interface

Usage:
  bgp-dashboard.py --asn <asn> -f <filename>
  bgp-dashboard.py --peers -f <filename>
  bgp-dashboard.py --stats -f <filename>
  bgp-dashboard.py --version

Options:
  -h --help     Show this screen.
  -f            File Name where "show ip bgp" data is located
  --asn         Get ASN details
  --peers       List of all directly connected BGP peers
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
                manager.print_asn_details(asn)
            elif args['--peers']:
                manager.print_details()
            elif args['--stats']:
                manager.print_stats()
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

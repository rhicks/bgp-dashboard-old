#!/usr/bin/env python3

"""BGP to SQLite

Usage:
  bgp2sql.py -f <filename>
  bgp2sql.py --version

Options:
  -h --help     Show this screen.
  -f            File Name where "show ip bgp" data is located
  --version     Show version.

"""

from docopt import docopt
import sys


def main(args):
    if args['<filename>']:
        try:
            filename = args['<filename>']
            data = get_data(filename)
            for line in data:
                print(line)
        except(FileNotFoundError):
            print("\nFile not found: {0}".format(filename), file=sys.stderr)

def parse_single_line(line, data_file   ):
    if not '::/' in line: # if the line isn't the route line then it must be the nexthop line
        nexthop = '{:<32}'.format(line[5:].split()[0]) # get the next hop
        other   = data_file.readline().rstrip() # read the next line to get the other data (metric, localpref, weight, as path, origin)
    else: # it must be the route line
        nexthop = data_file.readline().rstrip().lstrip() # read the next line to get the nexthop
        if len(nexthop.split()) > 1:
            other   = nexthop.split(' ', 1)[1] # get the other data, split on first space
            nexthop = '{:<71}'.format(nexthop.split()[0]) # get the next hop, should be first this time
        else:
            other   = data_file.readline().rstrip() # read the line after to get the other data
            nexthop = '{:<32}'.format(nexthop)
    return(nexthop + other)

def parse_double_line(line, data_file):
    nexthop = '{:<32}'.format(line.split()[1]) # get the next hop
    other   = data_file.readline().rstrip() # read the next line to get the other data
    return(nexthop + other)

def parse_multi_line(line):
    nexthop = '{:<76}'.format(line.split()[1]) # get the next hop after the prefix[0]
    other   = line.split('      ', 1)[1].rstrip() # get the other data, and strip most white space for alignment
    return(nexthop + other)

def get_data(filename):
    with open(filename) as data_file:
        for line in data_file:
            if '::/' in line:  # look for the "network prefix" in the line. This is the start of a new "chunk" of prefix/data.
                prefix = line[5:].split()[0] # prefix should always be the first field after the status
                while not '>' in line[0:5]: # a while loop to find the valid/best route (the one installed into the FIB)
                    line = data_file.readline() # keep reading lines from the data file until found
                status = line[0:5].lstrip().rstrip() # capture the status
                line = line[5:] # strip the status to make the line easier to work with
                if len(line.split()) == 1: # lines with only a single field
                    fixed_width_line = parse_single_line(line, data_file)
                if len(line.split()) == 2: # lines with two fields
                    fixed_width_line = parse_double_line(line, data_file)
                if len(line.split()) > 2: # lines with more than 2 items will have "all" the data on single line
                    fixed_width_line = parse_multi_line(line)
                next_hop_ip  = fixed_width_line.split(None, 1)[0]
                metric       = fixed_width_line[75:82].strip()
                local_pref   = fixed_width_line[82:89].strip()
                weight       = fixed_width_line[89:96].strip()
                as_path      = tuple(fixed_width_line[96:-1].split())
                route_origin = fixed_width_line[-1].strip()
                yield(status, prefix, next_hop_ip, metric, local_pref,
                      weight, as_path, route_origin)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='bgp2sql 0.0.1')
    # print(arguments)
    try:
        sys.exit(main(arguments))
    except(KeyboardInterrupt):
        print("\nExiting on user request.\n", file=sys.stderr)
        sys.exit(1)

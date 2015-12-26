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
import re

ipv4_regex = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

def main(args):
    if args['<filename>']:
        try:
            filename = args['<filename>']
            data = get_data(filename)
            for line in data:
                print(line)
        except(FileNotFoundError):
            print("\nFile not found: {0}".format(filename), file=sys.stderr)

def parse_single_line(line, data_file):
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

def ipv4_data(line):
    bad_lines = ('0.0.0.0', 'BGP') # ignore lines that could possibly return true
    for field in line.split():
        if field.startswith(bad_lines):
            return(False)
        elif ipv4_regex.match(field):
            return(True)

def build_full_prefix(status, prefix, line, ip_version):
    if ip_version == 4:
        metric_splice    = slice(18,26)
        localpref_splice = slice(26,33)
        weight_splice    = slice(33,40)
        aspath_splice    = slice(40,-1)
    if ip_version == 6:
        metric_splice    = slice(75,82)
        localpref_splice = slice(82,89)
        weight_splice    = slice(89,96)
        aspath_splice    = slice(96,-1)
    next_hop_ip  = line.split()[0]
    metric       = line[metric_splice].strip()
    local_pref   = line[localpref_splice].strip()
    weight       = line[weight_splice].strip()
    as_path      = list(line[aspath_splice].split())
    route_origin = line[-1].strip()
    return(status, prefix, next_hop_ip, metric, local_pref, weight, as_path, route_origin)

def parse_ipv6_data(line, data_file):
    ip_version = 6
    status_slice = slice(0,5)
    strip_status = slice(5,None)
    prefix = line[strip_status].split()[0] # prefix should always be the first field after the status
    while not '>' in line[status_slice]: # a while loop to find the valid/best route (the one installed into the FIB)
        line = data_file.readline() # keep reading lines from the data file until found
    status = line[status_slice].strip() # capture the status
    line = line[strip_status] # strip the status to make the line easier to work with
    if len(line.split()) == 1: # lines with only a single field
        fixed_width_line = parse_single_line(line, data_file)
    if len(line.split()) == 2: # lines with two fields
        fixed_width_line = parse_double_line(line, data_file)
    if len(line.split()) > 2: # lines with more than 2 items will have "all" the data on single line
        fixed_width_line = parse_multi_line(line)
    return(build_full_prefix(status, prefix, fixed_width_line, ip_version))

def parse_ipv4_data(line, data_file):
    ip_version = 4
    status_slice = slice(0,5)
    strip_status = slice(4,None)
    prefix = line[strip_status].split(' ')[1].strip()
    while not '>' in line[status_slice]:
        line = data_file.readline().strip()
    status = line[status_slice].strip()
    line = line[5:]
    if len(line.split()) == 1:
        line = data_file.readline()
    if (line.split()[0] == prefix):
        line = line.split(' ', 1)[1].strip()
    else:
        line = line.strip()
    return(build_full_prefix(status, prefix, line, ip_version))


def get_data(filename):
    ignored_lines = []
    strip_status = slice(4,None)
    with open(filename) as data_file:
        for line in data_file:
            if '::/' in line: # its ipv6
                yield(parse_ipv6_data(line, data_file))
            if ipv4_data(line) and ipv4_data(line[strip_status].split(' ')[1]):
                yield(parse_ipv4_data(line, data_file))
            else: # its crap
                ignored_lines.append(line)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='bgp2sql 0.0.1')
    # print(arguments)
    try:
        sys.exit(main(arguments))
    except(KeyboardInterrupt):
        print("\nExiting on user request.\n", file=sys.stderr)
        sys.exit(1)

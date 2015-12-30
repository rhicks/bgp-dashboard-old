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
import sqlite3
from datetime import datetime
import dns.resolver

database_file = './bgp.db' # location of SQL database
default_asn = 3701  # BGP ASN of the router where data was collected
ipv4_regex  = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


def main(args):
    if args['<filename>']:
        try:
            filename = args['<filename>']
            data = get_data(filename)
            #create_database()
            write_to_db(data, database_file)
        except(FileNotFoundError):
            print("\nFile not found: {0}".format(filename), file=sys.stderr)


def get_data(filename):
    ignored_lines = []
    with open(filename) as data_file:
        for line in data_file:
            if '::/' in line:  # its ipv6
                yield(parse_ipv6_data(line, data_file))
            if ipv4_data(line) and ipv4_data(line[4:].split(' ')[1]):  # its ipv4
                yield(parse_ipv4_data(line, data_file))
            else:  # its crap
                ignored_lines.append(line)

def write_to_db(data, database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # c.execute('delete from prefix')
    # c.execute('delete from autonomous_system')
    conn.commit()
    for line in data:
        status, prefix, next_hop_ip, metric, local_pref, weight, as_path, route_origin, origin_asn, next_hop_asn = line
        c.execute('select asn from autonomous_system where asn = ?', (origin_asn,))
        if c.fetchone():
            c.execute('insert or ignore into prefix values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (None, status, prefix, next_hop_ip, metric, local_pref, weight, str(as_path), route_origin, origin_asn, next_hop_asn, datetime.now(), datetime.now(), int(origin_asn)))
        else:
            c.execute('insert or ignore into autonomous_system values (?,?,?,?)', (origin_asn, asn_name_query(origin_asn), datetime.now(), datetime.now()))
            c.execute('insert or ignore into prefix values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (None, status, prefix, next_hop_ip, metric, local_pref, weight, str(as_path), route_origin, origin_asn, next_hop_asn, datetime.now(), datetime.now(), int(origin_asn)))
    conn.commit()

def asn_name_query(asn):
    query = 'AS' + str(asn) + '.asn.cymru.com'
    resolver = dns.resolver.Resolver()
    resolver.timeout = 1
    resolver.lifetime = 1
    try:
        answers = resolver.query(query, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                print(txt_string)
                return txt_string.split('|')[-1].split(",", 2)[0].strip()
    except:
        print("None")
        return("None")

def parse_ipv6_data(line, data_file):
    ip_version = 6
    status_slice = slice(0, 4)
    strip_status = slice(4, None)
    prefix = line[strip_status].split()[0]  # prefix is the first field
    while not '>' in line[status_slice]:  # find the "best" path
        line = data_file.readline()
    status = line[status_slice].strip()
    line = line[strip_status]  # strip the status for ease of use
    if len(line.split()) == 1:  # lines with only a single field
        fixed_width_line = parse_single_line(line, data_file)
    if len(line.split()) == 2:  # lines with two fields
        fixed_width_line = parse_double_line(line, data_file)
    if len(line.split()) > 2:  # all prefix data on single line
        fixed_width_line = parse_multi_line(line)
    return(build_full_prefix(status, prefix, fixed_width_line, ip_version))


def parse_ipv4_data(line, data_file):
    ip_version = 4
    status_slice = slice(0, 5)
    strip_status = slice(4, None)
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


def parse_single_line(line, data_file):
    if not '::/' in line:  # nexthop line
        nexthop = '{:<32}'.format(line[5:].split()[0])  # split for next hop
        other = data_file.readline().rstrip()  # read next line for other data
    else:  # route line
        nexthop = data_file.readline().rstrip().lstrip()  # read the next line
        if len(nexthop.split()) > 1:
            other = nexthop.split(' ', 1)[1]  # split for other data
            nexthop = '{:<71}'.format(nexthop.split()[0])  # split for next hop
        else:
            other = data_file.readline().rstrip()  # read next line for other data
            nexthop = '{:<32}'.format(nexthop)
    return(nexthop + other)


def parse_double_line(line, data_file):
    nexthop = '{:<32}'.format(line.split()[1])  # split for next hop
    other = data_file.readline().rstrip()  # read next line to get other data
    return(nexthop + other)


def parse_multi_line(line):
    nexthop = '{:<76}'.format(line.split()[1])  # split for next hop
    other = line.split('      ', 1)[1].rstrip() # number of spaces is important
    return(nexthop + other)


def ipv4_data(line):
    bad_lines = ('0.0.0.0', 'BGP')  # bad lines that could possibly return true
    for field in line.split():
        if field.startswith(bad_lines):
            return(False)
        elif ipv4_regex.match(field):
            return(True)


def build_full_prefix(status, prefix, line, ip_version):
    if ip_version == 4:
        metric_splice    = slice(18, 26)
        localpref_splice = slice(26, 33)
        weight_splice    = slice(33, 40)
        aspath_splice    = slice(40, -1)
    if ip_version == 6:
        metric_splice    = slice(73, 82)
        localpref_splice = slice(82, 89)
        weight_splice    = slice(89, 96)
        aspath_splice    = slice(96, -1)
    next_hop_ip  = line.split()[0]
    metric       = line[metric_splice].strip()
    local_pref   = line[localpref_splice].strip()
    weight       = line[weight_splice].strip()
    as_path      = list(line[aspath_splice].split())
    route_origin = line[-1].strip()
    if as_path:
        origin_asn = as_path[-1]
        next_hop_asn = as_path[0]
        if '{' in origin_asn:
            origin_asn = as_path[-2] # ignore atomic aggregates as destination
    else:
        origin_asn = default_asn
        next_hop_asn = None
    return(status, prefix, next_hop_ip, metric, local_pref, weight,
           as_path, route_origin, origin_asn, next_hop_asn)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='bgp2sql 0.0.1')
    # print(arguments)
    try:
        sys.exit(main(arguments))
    except(KeyboardInterrupt):
        print("\nExiting on user request.\n", file=sys.stderr)
        sys.exit(1)

# CREATE TABLE "autonomous_system" (
#   `asn`   INTEGER NOT NULL UNIQUE,
# 	`name`   VARCHAR(100),
# 	`created_timestamp`	DATETIME,
# 	`modified_timestamp`	DATETIME,
# 	PRIMARY KEY(asn)
# )

# CREATE TABLE "prefix" (
# 	`id`	INTEGER NOT NULL,
# 	`status`	VARCHAR(64),
# 	`prefix`	VARCHAR(128) UNIQUE,
# 	`next_hop_ip`	VARCHAR(64),
# 	`metric`	INTEGER,
# 	`local_pref`	INTEGER,
# 	`weight`	INTEGER,
# 	`as_path`	TEXT,
# 	`route_origin`	VARCHAR(64),
# 	`origin_asn`	INTEGER,
# 	`next_hop_asn`	INTEGER,
# 	`created_timestamp`	DATETIME,
# 	`modified_timestamp`	DATETIME,
# 	`autonomoussystem_asn`	INTEGER,
# 	PRIMARY KEY(id),
# 	FOREIGN KEY(`autonomoussystem_asn`) REFERENCES `autonomous_system`(`asn`)
# )

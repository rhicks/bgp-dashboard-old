#!/usr/bin/env python3

def parse_single_line(line):
    if not '::/' in line: # if the line isn't the route line then it must be the nexthop line
        nexthop = '{:<32}'.format(line[5:].split()[0]) # get the next hop
        other   = '{:<}'.format(data_file.readline().rstrip()) # read the next line to get the other data (metric, localpref, weight, as path, origin)
    else: # it must be the route line
        nexthop = data_file.readline().rstrip().lstrip() # read the next line to get the nexthop
        if len(nexthop.split()) > 1:
            other   = '{:<}'.format(nexthop.split(' ', 1)[1]) # get the other data, split on first space
            nexthop = '{:<71}'.format(nexthop.split()[0]) # get the next hop, should be first this time
        else:
            other   = '{:<}'.format(data_file.readline().rstrip()) # read the line after to get the other data
            nexthop = '{:<32}'.format(nexthop)
    return(nexthop, other)

def parse_double_line(line):
    nexthop = '{:<32}'.format(line.split()[1]) # get the next hop
    other   = '{:<}'.format(data_file.readline().rstrip()) # read the next line to get the other data
    return(nexthop, other)

def parse_multi_line(line):
    nexthop = '{:<76}'.format(line.split()[1]) # get the next hop after the prefix[0]
    other   = '{:<}'.format(line.split('      ', 1)[1]).rstrip() # get the other data, and strip most white space for alignment
    return(nexthop, other)


with open('ipv6-full.txt') as data_file:
    for line in data_file:
        if '::/' in line:  # look for the "network prefix" in the line. This is the start of a new "chunk" of prefix/data.
            prefix = line[5:].split()[0] # prefix should always be the first field after the status
            prefix = '{:<32}'.format(prefix)
            while not '>' in line[0:5]: # a while loop to find the valid/best route (the one installed into the FIB)
                line = data_file.readline() # keep reading lines from the data file until found
            status = line[0:5] # capture the status
            status = status.lstrip() # remove any whitespace to the left
            line = line[5:] # strip the status to make the line easier to work with
            if len(line.split()) == 1: # lines with only a single field
                print(status, prefix, parse_single_line(line))
            if len(line.split()) == 2: # lines with two fields
                print(status, prefix, parse_double_line(line))
            if len(line.split()) > 2: # lines with more than 2 items will have "all" the data on single line
                print(status, prefix, parse_multi_line(line))

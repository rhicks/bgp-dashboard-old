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
    return(nexthop + other)

def parse_double_line(line):
    nexthop = '{:<32}'.format(line.split()[1]) # get the next hop
    other   = '{:<}'.format(data_file.readline().rstrip()) # read the next line to get the other data
    return(nexthop + other)

def parse_multi_line(line):
    nexthop = '{:<76}'.format(line.split()[1]) # get the next hop after the prefix[0]
    other   = '{:<}'.format(line.split('      ', 1)[1]).rstrip() # get the other data, and strip most white space for alignment
    return(nexthop + other)

with open('ipv6-full.txt') as data_file:
    for line in data_file:
        if '::/' in line:  # look for the "network prefix" in the line. This is the start of a new "chunk" of prefix/data.
            prefix = line[5:].split()[0] # prefix should always be the first field after the status
            while not '>' in line[0:5]: # a while loop to find the valid/best route (the one installed into the FIB)
                line = data_file.readline() # keep reading lines from the data file until found
            status = line[0:5].lstrip().rstrip() # capture the status
            line = line[5:] # strip the status to make the line easier to work with
            if len(line.split()) == 1: # lines with only a single field
                fixed_width_line = parse_single_line(line)
            if len(line.split()) == 2: # lines with two fields
                fixed_width_line = parse_double_line(line)
            if len(line.split()) > 2: # lines with more than 2 items will have "all" the data on single line
                fixed_width_line = parse_multi_line(line)
            next_hop_ip  = fixed_width_line.split(None, 1)[0]
            metric       = fixed_width_line[75:82]
            local_pref   = fixed_width_line[82:89]
            weight       = fixed_width_line[89:96]
            as_path      = tuple(fixed_width_line[96:-1].split())
            route_origin = fixed_width_line[-1]
            print(status,prefix,next_hop_ip,metric,local_pref,weight,as_path,route_origin)

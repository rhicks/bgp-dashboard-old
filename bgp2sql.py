#!/usr/bin/env python3

with open('ipv6-full.txt') as data_file:
    for line in data_file:
        if '::/' in line:  # look for the "network prefix" in the line. This is the start of a new "chunk" of prefix/data.
            prefix  = line[5:].split()[0] # prefix should always be the first field after the status
            while not '>' in line[0:5]: # a while loop to find the valid/best route (the one installed into the FIB)
                line = data_file.readline() # keep reading lines from the data file until found
            status = line[0:5] # capture the status
            line = line[5:] # strip the status to make the line easier to work with
            if len(line.split()) == 1: # lines with only a single field
                if not '::/' in line: # if the line isn't the route line then it must be the nexthop line
                    nexthop = line[5:].split()[0] # get the next hop
                    other   = data_file.readline().rstrip() # read the next line to get the other data (metric, localpref, weight, as path, origin)
                    print(status.lstrip(), '{:<32}'.format(prefix), '{:<32}'.format(nexthop), '{:<}'.format(other)) # align the output for easy parsing
                else: # it must be the route line
                    nexthop = data_file.readline().rstrip().lstrip() # read the next line to get the nexthop
                    if len(nexthop.split()) > 1:
                        other   = nexthop.split(' ', 1)[1] # get the other data, split on first space
                        nexthop = nexthop.split()[0] # get the next hop, should be first this time
                        print(status.lstrip(), '{:<32}'.format(prefix), '{:<71}'.format(nexthop), '{:<}'.format(other)) # align the output for easy parsing
                    else:
                        other   = data_file.readline().rstrip() # read the line after to get the other data
                        print(status.lstrip(), '{:<32}'.format(prefix), '{:<32}'.format(nexthop), '{:<}'.format(other)) # align the output for easy parsing
            if len(line.split()) == 2: # lines with two fields
                nexthop = line.split()[1] # get the next hop
                other   = data_file.readline().rstrip() # read the next line to get the other data
                print(status.lstrip(), '{:<32}'.format(prefix), '{:<32}'.format(nexthop), '{:<}'.format(other))
            if len(line.split()) > 2: # lines with more than 2 items will have "all" the data on single line
                nexthop = line.split()[1] # get the next hop after the prefix[0]
                other   = line.split('      ', 1)[1] # get the other data, and strip most white space for alignment
                print(status.lstrip(), '{:<32}'.format(prefix), '{:<76}'.format(nexthop), '{:<}'.format(other.rstrip()))
        # test_for_network_line = line[4:]
        # possible_network = test_for_network_line.split(None)
        # if possible_network and '::/' in test_for_network_line.split(None)[0]:
        #     print(test_for_network_line.split(None)[0])
        # if '>' in status:
        #     # print(line + data_file.readline() + data_file.readline())
        #     print(line.rstrip())

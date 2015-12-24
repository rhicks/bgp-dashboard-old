#!/usr/bin/env python3

with open('ipv6-full.txt') as data_file:
    for line in data_file:
        if '::/' in line:  # look for the "network prefix" in the line
            prefix  = line[5:].split()[0] # prefix should always be the first field after the status
            while not '>' in line[0:5]:
                line = data_file.readline()
            status = line[0:5] # capture the status
            line = line[5:]
            if len(line.split()) == 1:
                if not '::/' in line:
                    # nexthop = data_file.readline().lstrip().rstrip()
                    nexthop = line[5:].split()[0]
                    other   = data_file.readline().rstrip()
                    print(status.lstrip(), '{:<32}'.format(prefix), '{:<32}'.format(nexthop), '{:<}'.format(other))
            if len(line.split()) == 2:
                nexthop = line.split()[1]
                other   = data_file.readline().rstrip()
                print(status.lstrip(), '{:<32}'.format(prefix), '{:<32}'.format(nexthop), '{:<}'.format(other))
            if len(line.split()) > 2:
                nexthop = line.split()[1]
                other   = line.split('      ', 1)[1]
                print(status.lstrip(), '{:<32}'.format(prefix), '{:<32}'.format(nexthop), '{:<}'.format(other.rstrip()))
        # test_for_network_line = line[4:]
        # possible_network = test_for_network_line.split(None)
        # if possible_network and '::/' in test_for_network_line.split(None)[0]:
        #     print(test_for_network_line.split(None)[0])
        # if '>' in status:
        #     # print(line + data_file.readline() + data_file.readline())
        #     print(line.rstrip())

BGP Dashboard
=============

A work in progress

##### Run tests: #####
 - cd $REPO/bgp-dashboard/src
 - python3 -m unittest

##### Brain Storming: #####
get a list of the "show ip bgp" data from a cisco router
  - cloginrc
  - paramiko
  - text file


The program should take a "show ip bgp" input and provide a list of all next hop entities.
Allow for tracking and notification of changes to a set of "monitored" ASN numbers.

e.g.

Website ideas:
A "realtime" dashboard with stats:
 - Total number of bgp peers
 - Total prefixes received from each peer
 - Number of routes using that BGP peer as a next hop
 - Next hop provider for a list of monitored ASN numbers
 - Configure alerts for monitored ASN numbers next hop provider changes (email, pager, etc...)
 - Ability to search for ASN/IP and find the next hop and full AS path


Thoughts:
 - Use BMP via ExaBGP to monitor realtime BGP changes
 - How to monitor routes in the routing table vs other "available" routes to the destination


Get Data
 The program should log into the router a $TIME interval and pull the "show ip bgp" and "show ip bgp ipv6 unicast" for parsing

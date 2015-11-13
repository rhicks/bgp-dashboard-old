import unittest
from ..reader import FileReaderIPv4
from ..autonomoussystem import AutonomousSystem
from collections import namedtuple


class FileReaderIPv4Test(unittest.TestCase):

    def setUp(self):
        self.reader = FileReaderIPv4("../bgp-data-full.txt")
        self.data = self.reader.get_data()

    def test_nothing(self):
        #route = (status, ipv4_prefix, next_hop_ipv4, metric, local_pref, weight, as_path, origin)
        for route in self.data:
            print(route)

    # def test_reader_should_return_a_tuple_of_data(self):
    #     # format: ipv4_prefix, dest-asn, next-hop-asn,
    #     #         weight, local_pref, metric, next_hop_ipv4, tuple(as_path)
    #     self.data = FileReaderIPv4.get_data(self, "../bgp-data.txt")
    #     test_data = next(self.data)  # get first tuple from the list to compare
    #     self.assertTupleEqual(
    #         ('1.0.0.0/24', '15169', '15169', '0', '1000', '0', '198.32.195.34', ('15169',)), test_data)
    #     #for line in self.data:
    #     #    print(line)
    #
    # def test_should_be_able_to_create_AutonomousSystem_object_from_data(self):
    #     self.data = FileReaderIPv4.get_data(self, "../bgp-data.txt")
    #     test_data = next(self.data)
    #     self.testasn = AutonomousSystem(test_data[1])
    #     self.assertIsInstance(self.testasn, AutonomousSystem)

    # def test_print_lines(self):
    #     self.data = FileReaderIPv4.get_data(self, "../bgp-dat.txt")
    #     Route = namedtuple('Route',
    #                         'ipv4_prefix asn next_hop_asn weight local_pref metric next_hop_ipv4 as_path')
    #     for line in self.data:
    #         myRoute = Route(ipv4_prefix=line[0],
    #                         asn=line[1],
    #                         next_hop_asn=line[2],
    #                         weight=line[3],
    #                         local_pref=line[4],
    #                         metric=line[5],
    #                         next_hop_ipv4=line[6],
    #                         as_path=line[7])
    #         print(myRoute)

    # lines = []
    # for line in raw_data:
    #     line = line.lstrip().rstrip()
    #     if "/" in line:
    #         if len(lines) == 0:
    #             lines.append(tuple(line.split()))
    #             continue
    #         else:
    #             return FileReaderIPv4.__build_data(lines)
    #             lines = []
    #             lines.append(tuple(line.split()))
    #     elif (line.startswith("*") or line.startswith("r i") or line.startswith("r>i")):
    #         lines.append(tuple(line.split()))
    #
    # def __build_data(lines):
    #     # ugly code to be refactored... someday
    #     for route in lines:
    #         if "/" in route[1]:
    #             ipv4_prefix = route[1]
    #         if "/" in route[2]:
    #             ipv4_prefix = route[2]
    #         if ">" in route[0] and len(route) > 2:
    #             asn = route[-2]
    #             if "/" in route[1]:
    #                 next_hop_asn = route[6]
    #                 weight = route[5]
    #                 local_pref = route[4]
    #                 metric = route[3]
    #                 next_hop_ipv4 = route[2]
    #                 as_path = route[6:-1]
    #             else:
    #                 next_hop_asn = route[5]
    #                 weight = route[4]
    #                 local_pref = route[3]
    #                 metric = route[2]
    #                 next_hop_ipv4 = route[1]
    #                 as_path = route[5:-1]
    #
    #     return(ipv4_prefix, asn, next_hop_asn, weight, local_pref, metric, next_hop_ipv4, as_path)
    #     # return(ipv4_prefix, weight, local_pref, metric, next_hop_ipv4,
    #     # as_path)
    #
    #
    # class FileReaderIPv4:
    #     """"Read 'show ip bgp' data from a text file and return a tuple to be processed"""
    #
    #     previous_line = None
    #
    #     def __parse_line(line, double_line):
    #         STATUS_START = 0
    #         STATUS_END = 3
    #         NETWORK_START = 4
    #         NETWORK_END = 21
    #         NEXTHOP_START = 21
    #         NEXTHOP_END = 40
    #         METRIC_START = 41
    #         METRIC_END = 46
    #         LOCALPREF_START = 47
    #         LOCALPREF_END = 55
    #         WEIGHT_START = 56
    #         WEIGHT_END = 61
    #         PATH_START = 62
    #         PATH_END = -2
    #         ORIGN = -1
    #
    #         if double_line:
    #             NETWORK_END += 1
    #             NEXTHOP_START += 1
    #             NEXTHOP_END += 1
    #             METRIC_START += 1
    #             METRIC_END += 1
    #             LOCALPREF_START += 1
    #             LOCALPREF_END += 1
    #             WEIGHT_START += 1
    #             WEIGHT_END += 1
    #             PATH_START += 1
    #
    #         status = line[STATUS_START:STATUS_END].lstrip().rstrip()
    #         ipv4_prefix = line[NETWORK_START:NETWORK_END].lstrip().rstrip()
    #         next_hop_ipv4 = line[NEXTHOP_START:NEXTHOP_END].lstrip().rstrip()
    #         metric = line[METRIC_START:METRIC_END].lstrip().rstrip()
    #         local_pref = line[LOCALPREF_START:LOCALPREF_END].lstrip().rstrip()
    #         weight = line[WEIGHT_START:WEIGHT_END].lstrip().rstrip()
    #         as_path = line[PATH_START:PATH_END].lstrip().rstrip()
    #         origin = line[ORIGN].lstrip().rstrip()
    #
    #         return(status, ipv4_prefix, next_hop_ipv4, metric, local_pref, weight, as_path, origin)
    #
    #     def __parse_input(line):
    #         PATH_START = 62
    #         PATH_END = -2
    #         as_path = line[PATH_START:PATH_END].lstrip().rstrip()
    #
    #         if as_path:
    #             FileReaderIPv4.previous_line = None
    #             return(FileReaderIPv4.__parse_line(line, False))
    #         else:
    #             if FileReaderIPv4.previous_line == None:
    #                 FileReaderIPv4.previous_line = line
    #             else:
    #                 line = FileReaderIPv4.previous_line + " " + line
    #                 return(FileReaderIPv4.__parse_line(line, True))
    #
    #     def get_data(filename):
    #         real_data_begins = False
    #         with open(filename, 'r') as data_file:
    #             for line in data_file:
    #                 line = line.lstrip().rstrip()
    #                 if real_data_begins:
    #                     yield FileReaderIPv4.__parse_input(line)
    #                 elif (line.startswith("*") or line.startswith("r i") or line.startswith("r>i")):
    #                     real_data_begins = True
    #                     yield FileReaderIPv4.__parse_input(line)
    #
    #
    # class FileReaderIPv6:
    #     """Read 'show ip bgp ipv6 unicast' data from a text file"""
    #     pass
    #
    #
    # class RouterReaderIPv4:
    #     """Read 'show ip bgp' data from a router login session"""
    #     pass
    #
    #
    # class RouterReaderIPv6:
    #     """Read 'show ip bgp ipv6 unicast' data from a router login session"""
    #     pass
    #
    #
    # class BMPReader:
    #     """Read BGP updates from a BGP Monitoring Protocol session"""
    #     pass

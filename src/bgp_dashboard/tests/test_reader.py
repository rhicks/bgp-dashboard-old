import unittest
from ..reader import FileReaderIPv4
from ..autonomoussystem import AutonomousSystem
from collections import namedtuple


class FileReaderIPv4Test(unittest.TestCase):

    def setUp(self):
        self.data = FileReaderIPv4.get_data(self, "../bgp-data.txt")

    def test_nothing(self):
        pass

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

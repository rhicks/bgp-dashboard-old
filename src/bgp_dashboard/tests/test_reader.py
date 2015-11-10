import unittest
from ..reader import FileReaderIPv4


class FileReaderIPv4Test(unittest.TestCase):

    def test_reader_should_return_a_tuple_of_data(self):
        # format: ipv4_prefix, dest-asn, next-hop-asn,
        #         weight, local_pref, metric, next_hop_ipv4, tuple(as_path)
        self.data = FileReaderIPv4.get_data(self, "../bgp-data.txt")
        test_data = next(self.data)  # get first tuple from the list to compare
        self.assertTupleEqual(('1.0.0.0/24', '15169', '15169', '0',
                               '1000', '0', '198.32.195.34', ('15169',)), test_data)
        # for line in self.data:
        #     print(line)

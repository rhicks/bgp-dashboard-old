import unittest
import ipaddress
from ..reader import FileReaderIPv4


class FileReaderIPv4Test(unittest.TestCase):

    def setUp(self):
        self.reader = FileReaderIPv4("../bgp-data.txt")
        self.data = self.reader.get_data()

    def test_all_fields_should_be_valid(self):
        for route in self.data:
            self.metric_field_should_be_valid(route)
            self.network_field_should_be_a_valid_ipv4_network(route)
            self.nexthop_field_should_be_a_valid_ipv4_address(route)
            self.metric_field_should_be_a_valid_number_or_None(route)
            self.localpref_field_should_be_a_valid_number_or_None(route)
            self.weight_field_should_be_a_valid_number_or_None(route)
            self.aspath_field_should_be_a_tuple_of_ints_or_None(route)
            self.origin_field_should_be_valid(route)
        self.ignored_lines_should_be_available_for_review()

    def metric_field_should_be_valid(self, route):
        valid_metric_options = ("*>i", "r>i", "*>")
        self.assertTrue(route[0] in valid_metric_options)

    def network_field_should_be_a_valid_ipv4_network(self, route):
        self.assertIsInstance(ipaddress.IPv4Network(
            route[1]), ipaddress.IPv4Network)

    def nexthop_field_should_be_a_valid_ipv4_address(self, route):
        self.assertIsInstance(ipaddress.IPv4Address(
            route[2]), ipaddress.IPv4Address)

    def metric_field_should_be_a_valid_number_or_None(self, route):
        if route[3]:
            self.assertIsInstance(int(route[3]), int)
        else:
            pass

    def localpref_field_should_be_a_valid_number_or_None(self, route):
        if route[4]:
            self.assertIsInstance(int(route[4]), int)
        else:
            pass

    def weight_field_should_be_a_valid_number_or_None(self, route):
        if route[5]:
            self.assertIsInstance(int(route[5]), int)
        else:
            pass

    def aspath_field_should_be_a_tuple_of_ints_or_None(self, route):
        if route[6]:
            for asn in route[6]:
                if "{" or "}" in asn:
                    asn = asn.strip("{")
                    asn = asn.strip("}")
                    if "," in asn:
                        asns = asn.split(",")
                        for asn in asns:
                            self.assertIsInstance(int(asn), int)
                self.assertIsInstance(int(asn), int)
            else:
                self.assertIsInstance(int(asn), int)
        else:
            pass

    def origin_field_should_be_valid(self, route):
        valid_origin_options = ("i", "?", "e")
        self.assertTrue(route[7] in valid_origin_options)

    def ignored_lines_should_be_available_for_review(self):
        ignored_input = self.reader.get_ignored_lines()
        self.assertTrue(any(line.startswith("BGP") for line in ignored_input))

    # def test_output_all_data(self):
    #     for route in self.data:
    #         print(route)
    #         pass

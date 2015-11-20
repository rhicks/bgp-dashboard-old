import unittest
import ipaddress
from ..autonomoussystem import AutonomousSystem


class AutonomousSystemTest(unittest.TestCase):

    def setUp(self):
        self.nero = AutonomousSystem(3701)
        self.nero.as_path = (6939, 4826, 38803, 56203)

    def test_a_new_autonomoussystem_should_require_an_asn(self):
        with self.assertRaises(TypeError):
            self.testasn = AutonomousSystem()

    def test_should_be_able_to_update_asn_number(self):
        self.testasn = AutonomousSystem(4600)
        self.testasn.asn = 4601
        self.assertEqual(4601, self.testasn.asn)

    def test_bad_asn_numbers_should_throw_a_ValueError(self):
        with self.assertRaises(ValueError):
            self.nero.asn = "badasnnumber416545464"

    # def test_bad_as_path_values_should_throw_a_ValueError(self):
    #     with self.assertRaises(ValueError):
    #         self.nero.as_path = ("aspath1234")

    def test_as_path_can_be_a_single_asn(self):
        self.nero.as_path = (15159,)
        self.assertEqual((15159,), self.nero.as_path)

    def test_should_be_able_to_set_the_ipv4_prefixes_as_a_list_of_networks(self):
        self.nero.ipv4_prefixes = ["1.0.4.0/24", "1.0.5.0/24", "1.0.6.0/24"]
        self.assertEqual(['1.0.4.0/24', '1.0.5.0/24', '1.0.6.0/24'],
            self.nero.ipv4_prefixes)

    def test_should_return_a_list_of_all_asn_ipv4_prefixes_as_ipv4_netowrks(self):
        self.nero.ipv4_prefixes = ["1.0.4.0/24", "1.0.5.0/24", "1.0.6.0/24"]
        self.assertIsInstance(ipaddress.IPv4Network(
            self.nero.ipv4_prefixes[0]), ipaddress.IPv4Network)

    def test_ipv4_prefixes_should_only_accept_valid_ipv4_networks(self):
        with self.assertRaises(ipaddress.AddressValueError):
            self.nero.ipv4_prefixes = ["1.0.4.0/24", "1.0.5.0/24", "1.0.6.0/42"]

    def test_should_be_able_to_set_the_ipv6_prefixes_as_a_list_of_networks(self):
        self.nero.ipv6_prefixes = ["2605:bc80::/32",]
        self.assertEqual(['2605:bc80::/32'], self.nero.ipv6_prefixes)

    def test_should_return_a_list_of_all_asn_ipv6_prefixes_as_ipv6_netowrks(self):
        self.nero.ipv6_prefixes = ["2605:bc80::/32",]
        self.assertIsInstance(ipaddress.IPv6Network(
            self.nero.ipv6_prefixes[0]), ipaddress.IPv6Network)

    def test_ipv6_prefixes_should_only_accept_valid_ipv6_networks(self):
        with self.assertRaises(ipaddress.AddressValueError):
            self.nero.ipv6_prefixes = ["2605:bc80::/32", "2605:bc80::/321"]

    def test_next_hop_asn_should_be_the_first_asn_in_the_as_path(self):
        self.assertEqual(6939, self.nero.next_hop_asn)

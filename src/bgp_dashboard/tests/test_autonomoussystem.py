import unittest
import ipaddress
from ..autonomoussystem import AutonomousSystem


class AutonomousSystemTest(unittest.TestCase):

    def setUp(self):
        self.nero = AutonomousSystem(3701)

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

    def test_should_be_able_add_ipv4_prefixes_to_the_list_of_networks(self):
        self.nero.add_ipv4_prefix("1.0.4.0/24")
        self.nero.add_ipv4_prefix("1.0.5.0/24")
        self.nero.add_ipv4_prefix("1.0.6.0/24")
        self.assertEqual(['1.0.4.0/24', '1.0.5.0/24', '1.0.6.0/24'],
            self.nero.get_ipv4_prefixes())

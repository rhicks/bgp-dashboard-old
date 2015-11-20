import unittest
import ipaddress
from ..ipv4prefix import IPv4Prefix


class IPv4PrefixTest(unittest.TestCase):

    def setUp(self):
        self.test_ipv4 = IPv4Prefix('*>i', '223.252.192.0/19', '4.53.200.1', '0', '1000', '0', ('3356', '1239', '4837', '45062'), 'i', 3701)

    def test_should_be_able_to_create_new_ipv4prefix(self):
        self.test_ipv4 = IPv4Prefix('*>i', '223.252.192.0/19', '4.53.200.1', '0', '1000', '0', ('3356', '1239', '4837', '45062'), 'i', 3701)
    #
    def test_should_be_able_to_get_as_path_from_ipv4prefix(self):
        self.assertEqual(('3356', '1239', '4837', '45062'), self.test_ipv4.as_path)
    
    # def test_bad_as_path_values_should_throw_a_ValueError(self):
    #     with self.assertRaises(ValueError):
    #         self.test_ipv4.as_path = ("aspath1234")

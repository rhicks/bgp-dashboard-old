import unittest
from ..autonomoussystem import AutonomousSystem


class AutonomousSystemTest(unittest.TestCase):

    def setUp(self):
        self.nero = AutonomousSystem("NERO")

    def test_asn_of_a_new_autonomoussystem_should_be_None(self):
        self.assertIsNone(self.nero.asn)

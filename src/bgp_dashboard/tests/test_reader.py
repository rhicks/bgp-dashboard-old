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
        #*>i 223.232.0.0/16 198.32.163.209           0   1050      0 4600 11164 10026 9498 45609 45609 45609 i
        Route = namedtuple('Route', 'status ipv4_prefix next_hop_ipv4 metric local_pref weight as_path origin')
        for route in self.data:
            status=route[0]
            ipv4_prefix = route[1]
            next_hop_ipv4 = route[2]
            metric = route[3]
            if route[4] == 0:
                local_pref = 0
                weight = route[4]
                as_path = route[5:-1]
            else:
                local_pref = route[4]
                weight = route[5]
                as_path = route[6:-1]
            origin= route[-1]
            myRoute = Route(status, ipv4_prefix, next_hop_ipv4, metric, local_pref, weight, as_path, origin)
            print(myRoute)

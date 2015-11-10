import unittest
from ..reader import FileReaderIPv4


class FileReaderIPv4Test(unittest.TestCase):

    # def test_file_should_exist_or_throw_error(self):
    #     pass

    def test_should_open_the_given_filename_to_get_data(self):
        self.data = FileReaderIPv4.get_data("../bgp-data.txt")
        print()
        for line in self.data:
            #print(line)
            for route in line:
                if "/" in route[1]:
                    print(route[1]) # network
                if "/" in route[2]:
                    print(route[2]) # network
                if ">" in route[0]:
                    print(route[-2]) # destination asn
                    if "/" in route[1]:
                        print(route[6]) # next_hop_asn
                    else:
                        print(route[5])
                # print(route)
                # break
            # if len(line) > 0:
            #     print(line[1])
     #self.assertIs(self.data, tuple)

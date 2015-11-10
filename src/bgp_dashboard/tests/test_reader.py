import unittest
from ..reader import FileReaderIPv4


class FileReaderIPv4Test(unittest.TestCase):

    # def test_file_should_exist_or_throw_error(self):
    #     pass

    def test_should_open_the_given_filename_to_get_data(self):
        self.data = FileReaderIPv4.get_data("../bgp-data.txt")
        for line in self.data:
            if len(line) > 0:
                print(line[1])
     #self.assertIs(self.data, tuple)

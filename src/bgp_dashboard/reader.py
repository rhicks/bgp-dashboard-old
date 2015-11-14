import re


class FileReaderIPv4:
    """"Read 'show ip bgp' data from a text file and return a tuple to be processed"""

    def __init__(self, filename):
        self.filename = filename
        self.STATUS_START = 0
        self.STATUS_END = 3
        self.ipv4_regex = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

    def line_is_not_garbage(self, line):
        if line == "":
            return False
        if line.startswith("*"):
            return True
        if line.startswith("r i"):
            return True
        if line.startswith("r>i"):
            return True
        if line.startswith("0.0.0.0"):
            return False
        if self.ipv4_regex.match(line.split()[0]):
            return True
        else:
            return False

    def line_is_multiline(self, line):
        if len(line.split()) < 4:
            return True

    def line_contains_the_network_prefix(self, line):
        route = line[4:]  # remove the route status info from the line
        if route.split(' ', 1)[0]:
            return True
        else:
            return False

    def line_is_the_best_route(self, line):
        status = line[self.STATUS_START:self.STATUS_END]
        # print(status)
        if ">" in status:
            return True

    def combine_best_route_and_network_prefix(self, data):
        good_prefix = None
        for line in data:
            status = line[self.STATUS_START:self.STATUS_END]
            route = line[4:]  # remove the route status info from the line
            prefix = route.split(' ', 1)[0]
            if not prefix:
                return(status.lstrip().rstrip() + " " + good_prefix.lstrip().rstrip() + " " + route.lstrip().rstrip())
            else:
                good_prefix = prefix

    def get_data(self):
        print()
        lines = []
        with open(self.filename, 'r') as data_file:
            for line in data_file:
                line = line.lstrip().rstrip()
                if self.line_is_not_garbage(line):
                    if self.line_is_multiline(line):
                        line = line + " " + data_file.readline().lstrip().rstrip()
                    if self.line_contains_the_network_prefix(line):
                        lines.append(line)
                        if self.line_is_the_best_route(line):
                            lines = []
                            yield line
                    else:
                        if self.line_is_the_best_route(line) and len(lines) > 0:
                            lines.append(line)
                            yield self.combine_best_route_and_network_prefix(lines)
                            lines = []


class FileReaderIPv6:
    """Read 'show ip bgp ipv6 unicast' data from a text file"""
    pass


class RouterReaderIPv4:
    """Read 'show ip bgp' data from a router login session"""
    pass


class RouterReaderIPv6:
    """Read 'show ip bgp ipv6 unicast' data from a router login session"""
    pass


class BMPReader:
    """Read BGP updates from a BGP Monitoring Protocol session"""
    pass

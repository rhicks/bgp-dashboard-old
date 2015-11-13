from collections import namedtuple

class FileReaderIPv4:
    """"Read 'show ip bgp' data from a text file and return a tuple to be processed"""

    def __init__(self, filename):
        self.filename = filename
        self.previous_line = None
        self.STATUS_START = 0
        self.STATUS_END = 3
        self.NETWORK_START = 4
        self.NETWORK_END = 21
        self.NEXTHOP_START = 21
        self.NEXTHOP_END = 40
        self.METRIC_START = 41
        self.METRIC_END = 46
        self.LOCALPREF_START = 47
        self.LOCALPREF_END = 55
        self.WEIGHT_START = 56
        self.WEIGHT_END = 61
        self.PATH_START = 62
        self.PATH_END = -2
        self.ORIGN = -1

    def __parse_line(self, line, double_line):
        if double_line:
            self.NETWORK_END += 1
            self.NEXTHOP_START += 1
            self.NEXTHOP_END += 1
            self.METRIC_START += 1
            self.METRIC_END += 1
            self.LOCALPREF_START += 1
            self.LOCALPREF_END += 1
            self.WEIGHT_START += 1
            self.WEIGHT_END += 1
            self.PATH_START += 1

        status = line[self.STATUS_START:self.STATUS_END].lstrip().rstrip()
        ipv4_prefix = line[self.NETWORK_START:self.NETWORK_END].lstrip().rstrip()
        next_hop_ipv4 = line[self.NEXTHOP_START:self.NEXTHOP_END].lstrip().rstrip()
        metric = line[self.METRIC_START:self.METRIC_END].lstrip().rstrip()
        local_pref = line[self.LOCALPREF_START:self.LOCALPREF_END].lstrip().rstrip()
        weight = line[self.WEIGHT_START:self.WEIGHT_END].lstrip().rstrip()
        as_path = line[self.PATH_START:self.PATH_END].lstrip().rstrip()
        origin = line[self.ORIGN].lstrip().rstrip()

        return(status, ipv4_prefix, next_hop_ipv4, metric, local_pref, weight, as_path, origin)

    def __parse_input(self, line):
        as_path = line[self.PATH_START:self.PATH_END].lstrip().rstrip()
        ipv4_prefix = line[self.NETWORK_START:self.NETWORK_END].lstrip().rstrip()

        if as_path:
            self.previous_line = None
            return(self.__parse_line(line, False))
        else:
            if self.previous_line == None:
                self.previous_line = line
            else:
                line = self.previous_line + " " + line
                return(self.__parse_line(line, True))

    def get_data(self):
        real_data_begins = False
        with open(self.filename, 'r') as data_file:
            lines = []
            for line in data_file:
                line = line.lstrip().rstrip()
                if real_data_begins:
                    yield self.__parse_input(line)
                elif (line.startswith("*") or line.startswith("r i") or line.startswith("r>i")):
                    real_data_begins = True
                    yield self.__parse_input(line)


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

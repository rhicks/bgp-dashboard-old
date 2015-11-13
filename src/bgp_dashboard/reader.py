from collections import namedtuple


class FileReaderIPv4:
    """"Read 'show ip bgp' data from a text file and return a tuple to be processed"""

    def __init__(self, filename):
        self.filename = filename
        self.previous_line = None
        self.__set_defaults()

    def __set_defaults(self):
        # sample: *>i 1.0.4.0/24       198.32.195.42            0   1000      0 6939 4826 38803 56203 i
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

    def __parse_line(self, line, line_type):
        self.__set_defaults()

        if line_type == "double_line":
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

        if line_type == "source_route":
            print(line + "ERROR RHICKS 2")
            self.PATH_START = 61

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
            if as_path == "0":
                return self.__parse_line(line, "source_route")
            else:
                return self.__parse_line(line, "double_line")
        else:
            if self.previous_line == None:
                self.previous_line = line
            else:
                line = self.previous_line + " " + line
                return self.__parse_line(line, "normal")


    def get_data(self):
        with open(self.filename, 'r') as data_file:
            real_data_begins = False
            lines = []

            for line in data_file:
                line = line.lstrip().rstrip()
                if real_data_begins:
                    try:
                        route = self.__parse_input(line)
                        if route[1]:
                            if len(lines) == 0:
                                lines.append(route)
                                continue
                            else:
                                if len(lines) > 1:
                                    templist = list(lines[1])
                                    templist[1] = lines[0][1]
                                    yield tuple(templist)
                                    lines = []
                                    lines.append(route)
                                else:
                                    #pass
                                    yield lines[0]
                        else:
                            if ">" in route[0]:
                                lines.append(route)
                    except ValueError as e:
                        print("RHICKS ERROR" + line + e)
                        pass
                elif (line.startswith("*") or line.startswith("r i") or line.startswith("r>i")):
                    real_data_begins = True
                    try:
                        route =  self.__parse_input(line)
                        print(route[0])
                        if ">" in route[0]:
                            lines.append(route)
                    except:
                        pass
            # for route in lines:
            #     print(route)
            #yield lines





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

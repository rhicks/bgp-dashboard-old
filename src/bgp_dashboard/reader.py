import re


class FileReaderIPv4(object):
    """Read 'show ip bgp' data from a text file and return a tuple to be processed
        Example Return:
        ('*>i', '223.252.192.0/19', '4.53.200.1', '0', '1000', '0', ('3356', '1239', '4837', '45062'), 'i')
        status, network, next_hop_ip, metric, local_pref, weight, as_path, origin
    """


    def __init__(self, filename):
        self.filename = filename
        self.ipv4_regex = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        self._garbage_lines = []

    def _line_is_not_garbage(self, line):
        valid_starts = ("*", "r i", "r>i")
        if line == "":
            return False
            self._garbage_lines.append(line)
        if line.startswith(valid_starts):
            return True
        if line.startswith("0.0.0.0"):
            self._garbage_lines.append(line)
            return False
        if self.ipv4_regex.match(line.split()[0]):
            return True
        else:
            self._garbage_lines.append(line)
            return False

    def _line_is_multiline(self, line):
        if len(line.split()) < 4:
            return True

    def _line_contains_the_network_prefix(self, line):
        route = line[4:]  # remove the status info from the line
        if route.split(' ', 1)[0]:
            return True
        else:
            return False

    def _line_is_the_best_route(self, line):
        status = line[0:3] # slice for status
        if ">" in status:
            return True

    def _combine_best_route_and_network_prefix(self, data):
        good_prefix = None
        for line in data:
            status = line[0:3] # slice for status
            route = line[4:]  # remove the status info from the line
            prefix = route.split(' ', 1)[0]
            if not prefix:
                return(status.lstrip().rstrip() +
                        " " + good_prefix.lstrip().rstrip() +
                        "    " + route.lstrip().rstrip())
            else:
                good_prefix = prefix

    def _split_line_into_route_fields(self, line):
        # This is the most fragile part of the program.
        # Cisco uses a mix of fixed and variable width fields.
        # Plus, any optional fields are completely missing from the output
        # making it impossible to split on space or any other character.
        # This code uses slices to pull the fixed width optional fields from
        # the output.  But first we remove the variable length fields from the
        # line (status, network).
        status = line[0:3] # slice for status
        line = line[4:]  # remove the route status info from the line
        network = line.split(None, 1)[0] # first split item for network
        nexthop = line.split(None, 2)[1] # second split item for nexthop
        end_of_line = line.split(None, 1)[1] # remove the network from the line
        metric = end_of_line[18:26] # slice for metric
        local_pref = end_of_line[27:33] # slice for local_pref
        weight = end_of_line[34:40] # slice for weight
        as_path = end_of_line[41:-1] # slice for as_path (41 to end of the line -1)A
        # aspath = [map(int, x) for x in tuple(as_path.split())]
        origin = end_of_line[-1] # slice for origin (-1 is last item)
        return (status.strip(),
                network.strip(),
                nexthop.strip(),
                metric.strip(),
                local_pref.strip(),
                weight.strip(),
                tuple(as_path.split()),
                origin.strip())

    def get_data(self):
        print()
        lines = []
        with open(self.filename, 'r') as data_file:
            for line in data_file:
                line = line.lstrip().rstrip()
                if self._line_is_not_garbage(line):
                    if self._line_is_multiline(line):
                        line = line + "  " + data_file.readline().lstrip().rstrip()
                    if self._line_contains_the_network_prefix(line):
                        lines.append(line)
                        if self._line_is_the_best_route(line):
                            lines = []
                            yield (self._split_line_into_route_fields(line))
                    else:
                        if self._line_is_the_best_route(line) and len(lines) > 0:
                            lines.append(line)
                            yield(self._split_line_into_route_fields(self._combine_best_route_and_network_prefix(lines)))
                            lines = []

    def get_ignored_lines(self):
        if len(self._garbage_lines) > 0:
            return tuple(self._garbage_lines)


class FileReaderIPv6(object):
    """Read 'show ip bgp ipv6 unicast' data from a text file"""
    pass


class RouterReaderIPv4(object):
    """Read 'show ip bgp' data from a router login session"""
    pass


class RouterReaderIPv6(object):
    """Read 'show ip bgp ipv6 unicast' data from a router login session"""
    pass


class BMPReader(object):
    """Read BGP updates from a BGP Monitoring Protocol session"""
    pass

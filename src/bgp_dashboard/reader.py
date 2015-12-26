import re

class FileReader(object):
    '''Read 'show ip bgp' data from a text file and return a tuple to be processed
        Example Return:
        ('*>i', '223.252.192.0/19', '4.53.200.1', '0', '1000', '0', ('3356', '1239', '4837', '45062'), 'i')
        status, network, next_hop_ip, metric, local_pref, weight, as_path, origin
    '''

    def __init__(self, filename):
        self.filename = filename
        self.default_asn = '3701'  # BGP ASN of the router where data was collected
        self.ipv4_regex  = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


    def get_data(self):
        ignored_lines = []
        with open(self.filename) as data_file:
            for line in data_file:
                if '::/' in line:  # its ipv6
                    yield(self.parse_ipv6_data(line, data_file))
                if self.ipv4_data(line) and self.ipv4_data(line[4:].split(' ')[1]):  # its ipv4
                    yield(self.parse_ipv4_data(line, data_file))
                else:  # its crap
                    ignored_lines.append(line)


    def parse_ipv6_data(self, line, data_file):
        ip_version = 6
        status_slice = slice(0, 5)
        strip_status = slice(5, None)
        prefix = line[strip_status].split()[0]  # prefix is the first field
        while not '>' in line[status_slice]:  # find the "best" path
            line = data_file.readline()
        status = line[status_slice].strip()
        line = line[strip_status]  # strip the status for ease of use
        if len(line.split()) == 1:  # lines with only a single field
            fixed_width_line = self.parse_single_line(line, data_file)
        if len(line.split()) == 2:  # lines with two fields
            fixed_width_line = self.parse_double_line(line, data_file)
        if len(line.split()) > 2:  # all prefix data on single line
            fixed_width_line = self.parse_multi_line(line)
        return(self.build_full_prefix(status, prefix, fixed_width_line, ip_version))


    def parse_ipv4_data(self, line, data_file):
        ip_version = 4
        status_slice = slice(0, 5)
        strip_status = slice(4, None)
        prefix = line[strip_status].split(' ')[1].strip()
        while not '>' in line[status_slice]:
            line = data_file.readline().strip()
        status = line[status_slice].strip()
        line = line[5:]
        if len(line.split()) == 1:
            line = data_file.readline()
        if (line.split()[0] == prefix):
            line = line.split(' ', 1)[1].strip()
        else:
            line = line.strip()
        return(self.build_full_prefix(status, prefix, line, ip_version))


    def parse_single_line(self, line, data_file):
        if not '::/' in line:  # nexthop line
            nexthop = '{:<32}'.format(line[5:].split()[0])  # split for next hop
            other = data_file.readline().rstrip()  # read next line for other data
        else:  # route line
            nexthop = data_file.readline().rstrip().lstrip()  # read the next line
            if len(nexthop.split()) > 1:
                other = nexthop.split(' ', 1)[1]  # split for other data
                nexthop = '{:<71}'.format(nexthop.split()[0])  # split for next hop
            else:
                other = data_file.readline().rstrip()  # read next line for other data
                nexthop = '{:<32}'.format(nexthop)
        return(nexthop + other)


    def parse_double_line(self, line, data_file):
        nexthop = '{:<32}'.format(line.split()[1])  # split for next hop
        other = data_file.readline().rstrip()  # read next line to get other data
        return(nexthop + other)


    def parse_multi_line(self, line):
        nexthop = '{:<76}'.format(line.split()[1])  # split for next hop
        other = line.split('      ', 1)[1].rstrip() # number of spaces is important
        return(nexthop + other)


    def ipv4_data(self, line):
        bad_lines = ('0.0.0.0', 'BGP')  # bad lines that could possibly return true
        for field in line.split():
            if field.startswith(bad_lines):
                return(False)
            elif self.ipv4_regex.match(field):
                return(True)


    def build_full_prefix(self, status, prefix, line, ip_version):
        if ip_version == 4:
            metric_splice    = slice(18, 26)
            localpref_splice = slice(26, 33)
            weight_splice    = slice(33, 40)
            aspath_splice    = slice(40, -1)
        if ip_version == 6:
            metric_splice    = slice(73, 82)
            localpref_splice = slice(82, 89)
            weight_splice    = slice(89, 96)
            aspath_splice    = slice(96, -1)
        next_hop_ip  = line.split()[0]
        metric       = line[metric_splice].strip()
        local_pref   = line[localpref_splice].strip()
        weight       = line[weight_splice].strip()
        as_path      = list(line[aspath_splice].split())
        route_origin = line[-1].strip()
        if as_path:
            origin_asn = as_path[-1]
            next_hop_asn = as_path[0]
            if '{' in origin_asn:
                origin_asn = as_path[-2] # ignore atomic aggregates as destination
        else:
            origin_asn = self.default_asn
            next_hop_asn = None
        return(status, prefix, next_hop_ip, metric, local_pref, weight,
               as_path, route_origin, origin_asn, next_hop_asn)

    # def _line_is_not_garbage(self, line):
    #     valid_starts = ('*', 'r i', 'r>i')
    #     if line == '':
    #         return False
    #         self._garbage_lines.append(line)
    #     if line.startswith(valid_starts):
    #         return True
    #     if line.startswith('0.0.0.0'):
    #         self._garbage_lines.append(line)
    #         return False
    #     if self.ipv4_regex.match(line.split()[0]) or self.ipv6_regex.match(line.split()[0]):
    #         return True
    #     else:
    #         self._garbage_lines.append(line)
    #         return False
    #
    # def _line_is_multiline(self, line):
    #     if len(line.split()) < 4:
    #         return True
    #
    # def _line_contains_the_network_prefix(self, line):
    #     route = line[4:]  # remove the status info from the line
    #     if route.split(' ', 1)[0]:
    #         return True
    #     else:
    #         return False
    #
    # def _line_is_the_best_route(self, line):
    #     status = line[0:3]  # slice for status
    #     if '>' in status:
    #         return True
    #
    # def _combine_best_route_and_network_prefix(self, data):
    #     good_prefix = None
    #     for line in data:
    #         status = line[0:3]  # slice for status
    #         route = line[3:]  # remove the status info from the line
    #         if not '>' in status:
    #             route = route.lstrip()
    #         prefix = route.split(' ', 1)[0]
    #         if not prefix:
    #             return(status.lstrip().rstrip() +
    #                    ' ' + good_prefix.lstrip().rstrip() +
    #                    '    ' + route.lstrip().rstrip())
    #         else:
    #             good_prefix = prefix
    #
    # def _split_line_into_route_fields(self, line):
    #     # This is the most fragile part of the program.
    #     # Cisco uses a mix of fixed and variable width fields.
    #     # Plus, any optional fields are completely missing from the output
    #     # making it impossible to split on space or any other character.
    #     # This code uses slices to pull the fixed width optional fields from
    #     # the output.  But first we remove the variable length fields from the
    #     # line (status, network).
    #     status = line[0:3]  # slice for status
    #     line = line[3:]  # remove the route status info from the line
    #     network = line.split(None, 1)[0]  # first split item for network
    #     nexthop = line.split(None, 2)[1]  # second split item for nexthop
    #     end_of_line = line.split(None, 1)[1] # remove the network from the line
    #     metric = end_of_line[18:26]  # slice for metric
    #     local_pref = end_of_line[27:33]  # slice for local_pref
    #     weight = end_of_line[34:40]  # slice for weight
    #     as_path = end_of_line[41:-1] # slice for as_path (41 to end of the line -1)
    #     origin = end_of_line[-1]  # slice for origin (-1 is last itemA
    #     as_path = re.sub(r'\{[^)]*\}', '', as_path) # remove AS-SET info from as_path
    #     return (status.strip(),
    #             network.strip(),
    #             nexthop.strip(),
    #             metric.strip(),
    #             local_pref.strip(),
    #             weight.strip(),
    #             tuple(as_path.split()),
    #             origin.strip())
    #
    # def _determine_data_type(self, line):
    #     for field in line.split():
    #         if self.ipv4_regex.match(field):
    #             self.unknown_data = False
    #             self.ipv4_data = True
    #         if self.ipv6_regex.match(field):
    #             self.unknown_data = False
    #             self.ipv6_data = True
    #
    #
    # def get_data(self):
    #     lines = []
    #     with open(self.filename, 'r') as data_file:
    #         for line in data_file:
    #             line = line.lstrip().rstrip()
    #             if self._line_is_multiline(line):
    #                 line = line + '  ' + data_file.readline().lstrip().rstrip()
    #                 if self._line_is_multiline(line):
    #                     line = line + '  ' + data_file.readline().lstrip().rstrip()
    #                     # print(line)
    #             if self._line_is_not_garbage(line):
    #                 if self.unknown_data:
    #                     self._determine_data_type(line)
    #                 if self.ipv4_data:
    #                     if self._line_contains_the_network_prefix(line):
    #                         lines.append(line)
    #                         if self._line_is_the_best_route(line):
    #                             lines = []
    #                             yield (self._split_line_into_route_fields(line), 4)
    #                     else:
    #                         if self._line_is_the_best_route(line) and len(lines) > 0:
    #                             lines.append(line)
    #                             yield(self._split_line_into_route_fields(self._combine_best_route_and_network_prefix(lines)), 4)
    #                             lines = []
    #                 if self.ipv6_data:
    #                     if self._line_contains_the_network_prefix(line):
    #                         lines.append(line)
    #                         if self._line_is_the_best_route(line):
    #                             lines = []
    #                             yield (self._split_line_into_route_fields(line), 6)
    #                     else:
    #                         if self._line_is_the_best_route(line) and len(lines) > 0:
    #                             lines.append(line)
    #                             yield(self._split_line_into_route_fields(self._combine_best_route_and_network_prefix(lines)), 6)
    #                             lines = []
    #
    # def get_ignored_lines(self):
    #     if len(self._garbage_lines) > 0:
    #         return tuple(self._garbage_lines)


class FileReaderIPv6(object):
    '''Read 'show ip bgp ipv6 unicast' data from a text file'''
    pass


class RouterReaderIPv4(object):
    '''Read 'show ip bgp' data from a router login session'''
    pass


class RouterReaderIPv6(object):
    '''Read 'show ip bgp ipv6 unicast' data from a router login session'''
    pass


class BMPReader(object):
    '''Read BGP updates from a BGP Monitoring Protocol session'''
    pass

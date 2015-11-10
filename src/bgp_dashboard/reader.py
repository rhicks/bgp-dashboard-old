class FileReaderIPv4:

    def __build_data(lines):
        for route in lines:
            if "/" in route[1]:
                ipv4_prefix = route[1]
            if "/" in route[2]:
                ipv4_prefix = route[2]
            if ">" in route[0]:
                asn = route[-2]
                if "/" in route[1]:
                    next_hop_asn = route[6]
                    weight = route[5]
                    local_pref = route[4]
                    metric = route[3]
                    next_hop_ipv4 = route[2]
                    as_path = route[6:-1]
                else:
                    next_hop_asn = route[5]
                    weight = route[4]
                    local_pref = route[3]
                    metric = route[2]
                    next_hop_ipv4 = route[1]
                    as_path = route[5:-1]

        return(ipv4_prefix, asn, next_hop_asn, weight, local_pref, metric, next_hop_ipv4, as_path)

    def get_data(self, filename):
        """Read 'show ip bgp' data from a text file"""
        with open(filename, 'r') as data_file:
            lines = []
            for line in data_file:
                line = line.lstrip().rstrip()
                if "/" in line:
                    if len(lines) == 0:
                        lines.append(tuple(line.split()))
                        continue
                    else:
                        yield FileReaderIPv4.__build_data(lines)
                        lines = []
                        lines.append(tuple(line.split()))
                elif line.startswith("*"):
                    lines.append(tuple(line.split()))


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

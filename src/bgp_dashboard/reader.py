class FileReaderIPv4:
    """Read 'show ip bgp' data from a text file"""
    def get_data(filename):
        with open(filename, 'r') as data_file:
            lines = []
            for line in data_file:
                line = line.lstrip().rstrip()
                if "/" in line:
                    if len(lines) == 0:
                        lines.append(tuple(line.split()))
                        continue
                    else:
                        yield lines
                        lines = []
                        lines.append(tuple(line.split()))
                elif line.startswith("*"):
                    lines.append(tuple(line.split()))
                # yield tuple(line.split())
                # yield lines


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

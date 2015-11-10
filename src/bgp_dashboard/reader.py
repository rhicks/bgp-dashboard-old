class FileReaderIPv4:
    """Read 'show ip bgp' data from a text file"""
    def get_data(filename):
        with open(filename, 'r') as data_file:
            for line in data_file:
                yield tuple(line.split())


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

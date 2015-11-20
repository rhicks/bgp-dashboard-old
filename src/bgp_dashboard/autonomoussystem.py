import ipaddress


class AutonomousSystem:
    dict_of_all = {}

    def __init__(self, asn):
        self.list_of_ipv4_prefixes = []
        self.asn = asn
        AutonomousSystem.dict_of_all[self.asn] = self

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def add_prefix(self, ipv4_prefix):
        self.list_of_ipv4_prefixes.append(ipv4_prefix)

    def _valid_as_path(self, as_path):
        # as_path must be empty or a tuple of integers
        if ((tuple(as_path) or not as_path)
        and all(isinstance(asn, int) for asn in as_path)):
            return True
        else:
            return False

    @property
    def asn(self):
        return self._asn

    @asn.setter
    def asn(self, asn):
        if int(asn):
            self._asn = asn
        else:
            raise ValueError("ASN should be a positive number")

    @property
    def as_path(self):
        return self._as_path

    @as_path.setter
    def as_path(self, as_path):
        if self._valid_as_path(as_path):
            self._as_path = as_path
        else:
            raise ValueError("Invalid AS Path")

    @property
    def ipv4_prefixes(self):
        return self._ipv4_prefixes

    @ipv4_prefixes.setter
    def ipv4_prefixes(self, ipv4_prefixes):
        for prefix in ipv4_prefixes:
            try:
                ipaddress.IPv4Network(prefix)
                self._ipv4_prefixes = ipv4_prefixes
            except:
                raise ipaddress.AddressValueError("Invalid IPv4 Network")

    @property
    def ipv6_prefixes(self):
        return self._ipv6_prefixes

    @ipv6_prefixes.setter
    def ipv6_prefixes(self, ipv6_prefixes):
        for prefix in ipv6_prefixes:
            try:
                ipaddress.IPv6Network(prefix)
                self._ipv6_prefixes = ipv6_prefixes
            except:
                raise ipaddress.AddressValueError("Invalid IPv6 Network")

    @property
    def next_hop_asn(self):
        return self.as_path[0]

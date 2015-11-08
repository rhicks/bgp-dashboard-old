import ipaddress
# AS
# - attributes
#   - asn
#   - ipv4_prefixes
#   - as-path
#   - next-hop-ip
#   - next-hop-asn


class AutonomousSystem:

    def __init__(self, asn):
        self.asn = asn
        # self.as_path = ()
        # self.ipv4_prefixes = []
        # self.ipv6_prefixes = []
        # self.next_hop_ipv4 = None
        # self.next_hop_ipv6 = None
        # # self.next_hop_asn = None

    def _valid_as_path(self, as_path):
        if ((tuple(as_path) or not as_path)
        and all(isinstance(asn, int) for asn in as_path)):
            return True
        else:
            return False

    @property
    def asn(self):
        return self.__asn

    @asn.setter
    def asn(self, asn):
        if int(asn):
            self.__asn = asn
        else:
            raise ValueError("ASN should be a positive number")

    @property
    def as_path(self):
        return self.__as_path

    @as_path.setter
    def as_path(self, as_path):
        if self._valid_as_path(as_path):
            self.__as_path = as_path
        else:
            raise ValueError("Invalid AS Path")

    @property
    def ipv4_prefixes(self):
        return self.__ipv4_prefixes

    @ipv4_prefixes.setter
    def ipv4_prefixes(self, ipv4_prefixes):
        for prefix in ipv4_prefixes:
            try:
                ipaddress.IPv4Network(prefix)
                self.__ipv4_prefixes = ipv4_prefixes
            except:
                raise ipaddress.AddressValueError("Invalid IPv4 Network")

    @property
    def ipv6_prefixes(self):
        return self.__ipv6_prefixes

    @ipv6_prefixes.setter
    def ipv6_prefixes(self, ipv6_prefixes):
        for prefix in ipv6_prefixes:
            try:
                ipaddress.IPv6Network(prefix)
                self.__ipv6_prefixes = ipv6_prefixes
            except:
                raise ipaddress.AddressValueError("Invalid IPv6 Network")

    @property
    def next_hop_asn(self):
        return self.as_path[0]

    # @next_hop_asn.setter
    # def next_hop_asn(self, next_hop_asn):
    #     if len(self.as_path) > 0:
    #         self.__next_hop_asn = self.as_path[0]

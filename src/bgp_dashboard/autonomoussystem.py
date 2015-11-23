import ipaddress


class AutonomousSystem(object):
    dict_of_all = {}

    def __init__(self, asn):
        self.__list_of_ipv4_prefixes = []
        self.asn = asn
        AutonomousSystem.dict_of_all[self.asn] = self

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def add_ipv4_prefix(self, ipv4_prefix):
        self.__list_of_ipv4_prefixes.append(ipv4_prefix)

    def get_ipv4_prefixes(self):
        return self.__list_of_ipv4_prefixes

    @property
    def asn(self):
        return self._asn

    @asn.setter
    def asn(self, asn):
        if int(asn):
            self._asn = asn
        else:
            raise ValueError("ASN should be a positive number")

import re

class IPv4Prefix:
    count = 0

    def __init__(self, status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin, default_asn):
        IPv4Prefix.count = IPv4Prefix.count + 1
        self.status = status
        self.prefix = prefix
        self.next_hop_ip = next_hop_ip
        self.metric = metric
        self.local_pref = local_pref
        self.weight = weight
        self.as_path = as_path
        self.origin = origin
        self.default_asn = default_asn
        # self.destination_asn = None
        if self.as_path:
            self.next_hop_asn = self.as_path[0]
            # if "{" in self.as_path[-1]:
            #     self.destination_asn = self.as_path[-2]
            # else:
            #     self.destination_asn = self.as_path[-1]
        else:
            self.next_hop_asn = None
            # self.destination_asn = default_asn

    def __str__(self):
        return str(self.__dict__)

    def _valid_as_path(self, aspath):
        # as_path must be empty or a tuple of integers
        if (list(aspath) or not aspath):
        # and all(isinstance(asn, int) for asn in as_path)):
            return True
        else:
            return False

    @staticmethod
    def get_count():
        return IPv4Prefix.count

    # @property
    # def next_hop_asn(self):
    #     return self._next_hop_asn
    #
    # @next_hop_asn.setter
    # def next_hop_asn(self):
    #     if self.as_path:
    #         self._next_hop_asn = self.as_path[0]
    #     else:
    #         self._next_hop_asn = None
    #
    @property
    def as_path(self):
        return self._as_path

    @as_path.setter
    def as_path(self, as_path):
        if as_path:
            if "{" in as_path[-1]:
                self._as_set = as_path.pop()
                self._as_path = as_path
            if self._valid_as_path(as_path):
                self._as_path = as_path
            else:
                raise ValueError("Invalid AS Path")
            if any("{" in asn for asn in list(as_path)):
                # print(as_path)
                # Need to fix this code.  An AS-SET in the middle of an AS-Path
                # Only a single instance of the design in the entire BGP table
                pass
        else:
            self._as_path = None
    #
    # # @destination_asn.setter
    # # def destination_asn(self):
    # #     print(self._as_path)
    # #     if self._as_path:
    # #         self._destination_asn = self._as_path[-1]
    # #     else:
    # #         self._destination_asn = 3701
    #
    @property
    def destination_asn(self):
        if self.as_path:
            return self.as_path[-1]
        else:
            return self.default_asn

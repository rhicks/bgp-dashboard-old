class IPv4Prefix(object):
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

    def __str__(self):
        return str(self.__dict__)

    @staticmethod
    def get_count():
        return IPv4Prefix.count

    def _valid_as_path(self, as_path):
        # as_path must be empty or a tuple of integers
        if (tuple(as_path) or not as_path):
            if all(int(asn) for asn in as_path):
                return True
        else:
            return False

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
    def destination_asn(self):
        if self._as_path:
            if "{" in self._as_path[-1]:
                return self._as_path[-2]
            else:
                return self._as_path[-1]
        else:
            return self.default_asn

    @property
    def next_hop_asn(self):
        if self._as_path:
            return self.as_path[0]
        else:
            return None

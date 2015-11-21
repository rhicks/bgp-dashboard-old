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
        # self.destination_asn = None
        # if self.as_path:
        #     self.next_hop_asn = self.as_path[0]
        #     if "{" in self.as_path[-1]:
        #         self.destination_asn = self.as_path[-2]
        #     else:
        #         self.destination_asn = self.as_path[-1]
        # else:
        #     self.next_hop_asn = None
        #     self.destination_asn = default_asn

    def __str__(self):
        return str(self.__dict__)

    @staticmethod
    def get_count():
        return IPv4Prefix.count

    def _valid_as_path(self, as_path):
        # as_path must be empty or a tuple of integers
        if (tuple(as_path) or not as_path):
        #and all(isinstance(asn, int) for asn in as_path)):
            return True
        else:
            return False

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        self._prefix = prefix

    @property
    def next_hop_ip(self):
        return self._next_hop_ip

    @next_hop_ip.setter
    def next_hop_ip(self, next_hop_ip):
        self._next_hop_ip = next_hop_ip

    @property
    def metric(self):
        return self._metric

    @metric.setter
    def metric(self, metric):
        self._metric = metric

    @property
    def local_pref(self):
        return self._local_pref

    @local_pref.setter
    def local_pref(self, local_pref):
        self._local_pref = local_pref

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._weight = weight

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
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, origin):
        self._origin = origin

    @property
    def default_asn(self):
        return self._default_asn

    @default_asn.setter
    def default_asn(self, default_asn):
        self._default_asn = default_asn

    @property
    def destination_asn(self):
        if self._as_path:
            if "{" in self._as_path[-1]:
                return self._as_path[-2]
            else:
                return self._as_path[-1]
        else:
            return self._default_asn

    @property
    def next_hop_asn(self):
        if self._as_path:
            return self.as_path[0]
        else:
            return None

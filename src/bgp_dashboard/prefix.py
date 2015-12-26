class Prefix(object):
    count = 0

    def __init__(self, status, prefix, next_hop_ip, metric, local_pref, weight, as_path, route_origin, origin_asn, next_hop_asn):
        Prefix.count = Prefix.count + 1
        self.status = status
        self.prefix = prefix
        self.next_hop_ip = next_hop_ip
        self.metric = metric
        self.local_pref = local_pref
        self.weight = weight
        self.as_path = as_path
        self.route_origin = route_origin
        self.origin_asn = origin_asn
        self.next_hop_asn = next_hop_asn

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def get_count():
        return Prefix.count

    def _valid_as_path(self, as_path):
        # as_path must be empty or a tuple of integers
        if (list(as_path) or not as_path):
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
            raise ValueError('Invalid AS Path')

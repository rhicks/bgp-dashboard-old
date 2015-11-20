class IPv4Prefix:
    count = 0

    def __init__(self, status, prefix, next_hop_ip, metric, local_pref, weight, as_path, origin, manager):
        IPv4Prefix.count = IPv4Prefix.count + 1
        self.status = status
        self.prefix = prefix
        self.next_hop_ip = next_hop_ip
        self.metric = metric
        self.local_pref = local_pref
        self.weight = weight
        self.as_path = as_path
        self.origin = origin
        if self.as_path:
            self.next_hop_asn = self.as_path[0]
            if "{" in self.as_path[-1]:
                self.destination_asn = self.as_path[-2]
            else:
                self.destination_asn = self.as_path[-1]
        else:
            self.next_hop_asn = None
            self.destination_asn = manager.default_asn

    def __str__(self):
        return str(self.__dict__)

    @staticmethod
    def get_count():
        return IPv4Prefix.count

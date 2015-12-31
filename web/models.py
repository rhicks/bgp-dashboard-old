import dns.resolver
from datetime import datetime
from app import db

class AutonomousSystem(db.Model):
    asn = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100))
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    prefixes = db.relationship('Prefix', backref='autonomous_system', lazy='joined')

    def __init__(self, *args, **kwargs):
        super(AutonomousSystem, self).__init__(*args, **kwargs)
        # self.asn  = int(asn)
        # self.name = self._asn_name_query(asn)

    def __repr__(self):
        return '<ASN: %s>' % self.asn

    # @property
    # def asn(self):
    #     return self._asn
    #
    # @asn.setter
    # def asn(self, asn):
    #     if int(asn):
    #         self._asn = asn
    #     else:
    #         raise ValueError('ASN should be a positive number')
    #
    # def _asn_name_query(self, asn):
    #      query = 'AS' + str(asn) + '.asn.cymru.com'
    #      answers = dns.resolver.query(query, 'TXT')
    #      for rdata in answers:
    #          for txt_string in rdata.strings:
    #              return txt_string.split('|')[-1].split(",", 2)[0].strip()


class Prefix(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    status = db.Column(db.String(64))
    prefix = db.Column(db.String(128), unique=True)
    next_hop_ip = db.Column(db.String(64))
    metric = db.Column(db.Integer)
    local_pref = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    as_path = db.Column(db.Text)
    route_origin = db.Column(db.String(64))
    origin_asn = db.Column(db.Integer)
    next_hop_asn  = db.Column(db.Integer)
    created_timestamp  = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    autonomoussystem_asn = db.Column(db.Integer, db.ForeignKey('autonomous_system.asn'))
    ip_version = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super(Prefix, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Prefix: %s>' % self.prefix

    def __str__(self):
        return str(self.__dict__)

    #
    # def _valid_as_path(self, as_path):
    #     # as_path must be empty or a tuple of integers
    #     if (list(as_path) or not as_path):
    #         return True
    #     else:
    #         return False
    #
    # @property
    # def as_path(self):
    #     return self._as_path
    #
    # @as_path.setter
    # def as_path(self, as_path):
    #     if self._valid_as_path(as_path):
    #         self._as_path = as_path
    #     else:
    #         raise ValueError('Invalid AS Path')

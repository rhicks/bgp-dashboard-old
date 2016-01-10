from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table
from sqlalchemy import func
from datetime import datetime
import dns.resolver
import dns.reversename
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/bgp.db'
db = SQLAlchemy(app)

class ASN(db.Model):
    __tablename__ = 'autonomous_system'

    asn = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100))
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    verified_timestamp = db.Column(db.DateTime, default=datetime.now)
    origin_prefixes = db.relationship('Prefix', foreign_keys='Prefix.origin_asn', lazy='dynamic')
    best_routes = db.relationship('Prefix', foreign_keys='Prefix.next_hop_asn', lazy='dynamic')

    # def __init__(self, asn, name):
    #     self.asn = asn
    #     self.name = name

    def asn_name_query(self, asn):
        if self.name is None or self.name == str(asn):
            if 64512 <= asn <= 65534:
                self.name = "RFC6996 - Private Use ASN"
                db.session.add(self)
                db.session.commit()
                return("RFC6996 - Private Use ASN")
            else:
                query = 'AS' + str(asn) + '.asn.cymru.com'
                resolver = dns.resolver.Resolver()
                resolver.timeout = 1
                resolver.lifetime = 1
                try:
                    answers = resolver.query(query, 'TXT')
                    for rdata in answers:
                        for txt_string in rdata.strings:
                            self.name = txt_string.split('|')[-1].split(",", 2)[0].strip()
                            db.session.add(self)
                            db.session.commit()
                            return txt_string.split('|')[-1].split(",", 2)[0].strip()
                except:
                    self.name = None
                    db.session.add(self)
                    db.session.commit()
                    return("(DNS Error)")
        else:
            return self.name

    def reverse_dns_query(self, ip):
        addr = dns.reversename.from_address(ip)
        resolver = dns.resolver.Resolver()
        resolver.timeout = 1
        resolver.lifetime = 1
        try:
            print(str(resolver.query(addr,"PTR")[0])[:-1])
            return str(resolver.query(addr,"PTR")[0])[:-1]
        except:
            return("(DNS Error)")

    def peering_sessions(self, asn):
        counter = []
        stuff = db.session.execute('select distinct next_hop_ip from prefix where next_hop_asn == %d' % asn.asn)
        for thing in stuff:
            counter.append(thing[0])
            #print(thing[0])
        return(counter)

    def ipv4_peer_count(self, asn):
        cursor = db.session.execute('select count(distinct next_hop_ip) from prefix where ip_version == 4 and next_hop_asn == %d' % asn.asn)
        return cursor.scalar()

    def ipv6_peer_count(self, asn):
        cursor = db.session.execute('select count(distinct next_hop_ip) from prefix where ip_version == 6 and next_hop_asn == %d' % asn.asn)
        return cursor.scalar()

    def ipv4_origin_count(self, asn):
        cursor = db.session.execute('select count(prefix) from prefix where ip_version == 4 and origin_asn == %d' % asn.asn)
        return cursor.scalar()

    def ipv6_origin_count(self, asn):
        cursor = db.session.execute('select count(prefix) from prefix where ip_version == 6 and origin_asn == %d' % asn.asn)
        return cursor.scalar()

    def ipv4_transit_count(self, asn):
        cursor = db.session.execute('select count(prefix) from prefix where ip_version == 4 and next_hop_asn == %d' % asn.asn)
        return cursor.scalar()

    def ipv6_transit_count(self, asn):
        cursor = db.session.execute('select count(prefix) from prefix where ip_version == 6 and next_hop_asn == %d' % asn.asn)
        return cursor.scalar()

    def __repr__(self):
        return '<ASN: %s>' % self.asn


class Prefix(db.Model):
    __tablename__ = 'prefix'
    id = db.Column(db.Integer, primary_key=True, index=True)
    ip_version = db.Column(db.Integer)
    status = db.Column(db.String(64))
    prefix = db.Column(db.String(64), index=True)
    next_hop_ip = db.Column(db.String(64), index=True)
    metric = db.Column(db.Integer)
    local_pref = db.Column(db.Integer)
    weight  = db.Column(db.Integer)
    as_path = db.Column(db.Text)
    route_origin = db.Column(db.String(64))
    origin_asn  = db.Column(db.Integer, db.ForeignKey('autonomous_system.asn'), index=True)
    next_hop_asn = db.Column(db.Integer, db.ForeignKey('autonomous_system.asn'), index=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    verified_timestamp = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Prefix: %s>' % self.prefix

@app.route('/')
def index():
    autonomoussystems = db.session.query(ASN)
    prefixes = db.session.query(Prefix)
    ipv4_prefixes = prefixes.filter(Prefix.ip_version == 4)
    ipv6_prefixes = prefixes.filter(Prefix.ip_version == 6)
    nexthop_asns = db.session.query(Prefix.next_hop_asn.distinct())
    nexthop_ips  = db.session.query(Prefix.next_hop_ip.distinct())
    peers = autonomoussystems.filter(ASN.asn.in_(nexthop_asns))
    return render_template('home.html', **locals())

@app.route('/asn/<asn>')
def asn(asn):
    autonomous_system = ASN.query.filter(ASN.asn == asn).first()
    return render_template('asn.html', **locals())

if __name__ == '__main__':
    app.run(debug=True)

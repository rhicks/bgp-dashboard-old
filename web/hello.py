from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table
from sqlalchemy import func
from datetime import datetime
import dns.resolver

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

    def asn_name_query(asn):
        query = 'AS' + str(asn.asn) + '.asn.cymru.com'
        #print(query) ## enable for debuging
        resolver = dns.resolver.Resolver()
        resolver.timeout = 1
        resolver.lifetime = 1
        try:
            answers = resolver.query(query, 'TXT')
            for rdata in answers:
                for txt_string in rdata.strings:
                    #print(txt_string) ## enable for debuging
                    return txt_string.split('|')[-1].split(",", 2)[0].strip()
        except:
            #print("None") ## enable for debuging
            return("None")

    def peering_sessions(self, asn):
        counter = []
        stuff = db.session.execute('select distinct next_hop_ip from prefix where next_hop_asn == %d' % asn.asn)
        for thing in stuff:
            counter.append(thing)
        return(len(counter))

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

if __name__ == '__main__':
    app.run(debug=True)

from flask import render_template
from app import app
from app import db
from models import AutonomousSystem, Prefix
from sqlalchemy import func, distinct
from helpers import object_list

@app.route('/')
def homepage():
    autonomoussystems = db.session.query(AutonomousSystem.asn, AutonomousSystem.name)
    prefixes = db.session.query(Prefix.ip_version)
    ipv4_prefixes = prefixes.filter(Prefix.ip_version == 4)
    ipv6_prefixes = prefixes.filter(Prefix.ip_version == 6)
    nexthop_asns = db.session.query(Prefix.next_hop_asn.distinct())
    nexthop_ips  = db.session.query(Prefix.next_hop_ip.distinct())
    peers = autonomoussystems.filter(AutonomousSystem.asn.in_(nexthop_asns))

    return render_template('home.html',
                            autonomoussystems=autonomoussystems,
                            prefixes=prefixes,
                            ipv4_prefixes=ipv4_prefixes,
                            ipv6_prefixes=ipv6_prefixes,
                            nexthop_ips=nexthop_ips,
                            peers=peers)

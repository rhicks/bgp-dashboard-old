from flask import render_template
from app import app
from app import db
from models import AutonomousSystem, Prefix
from sqlalchemy import func, distinct

@app.route('/')
def homepage():
    autonomoussystems = AutonomousSystem.query.order_by(AutonomousSystem.asn.asc())
    prefixes = Prefix.query.order_by(Prefix.ip_version.asc())
    ipv4_prefixes = Prefix.query.filter(Prefix.ip_version == 4)
    ipv6_prefixes = Prefix.query.filter(Prefix.ip_version == 6)
    peers = db.session.query(Prefix.next_hop_asn.distinct()).order_by(Prefix.next_hop_asn)
    return render_template('home.html',
                            autonomoussystems=autonomoussystems,
                            prefixes=prefixes,
                            ipv4_prefixes=ipv4_prefixes,
                            ipv6_prefixes=ipv6_prefixes,
                            peers=peers)

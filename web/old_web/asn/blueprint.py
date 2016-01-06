from flask import Blueprint
from helpers import object_list
from models import AutonomousSystem, Prefix

asn = Blueprint('asn', __name__, template_folder='templates')

@asn.route('/')
def index():
    asn = AutonomousSystem.query.order_by(AutonomousSystem.asn.asc())
    # autonomoussystems = db.session.query(AutonomousSystem)
    return object_list('asn/index.html', asn)

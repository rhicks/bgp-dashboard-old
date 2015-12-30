import os

class Configuration():
    DEBUG = True
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/../database/bgp.db' % APPLICATION_DIR

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import Configuration  # import our configuration data.

app = Flask(__name__)
app.config.from_object(Configuration)  # use values from our Configuration object.
db = SQLAlchemy(app)

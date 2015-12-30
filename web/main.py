from app import app, db
import models
import views

from asn.blueprint import asn
app.register_blueprint(asn, url_prefix='/asn')

if __name__ == '__main__':
    app.run()

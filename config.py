import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import logging
basedir = os.path.abspath(os.path.dirname(__file__))
# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)
# Get the underlying Flask app instance
app = connex_app.app
# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_ECHO'] = True
#NOICE EGRISH 'ERE M8
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shedule.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Create the SQLAlchemy db instance
db = SQLAlchemy(app)
#db.init_app(app)
logging.basicConfig(level=logging.DEBUG)
# Initialize Marshmallow
ma = Marshmallow(app)
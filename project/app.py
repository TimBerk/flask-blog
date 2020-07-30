from flask import Flask
from flask_ckeditor import CKEditor
from flask_moment import Moment

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security

from config import Configuration

app = Flask(__name__, static_folder='static')
app.config.from_object(Configuration)

ckeditor = CKEditor(app)
moment = Moment(app)

# Work with migration
from shared import db
from models import User, Role

# Flask security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

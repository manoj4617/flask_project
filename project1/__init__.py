from flask import *
from flask_sqlalchemy import *
from flask_login import LoginManager
 
app = Flask(__name__, static_url_path='/static')
app.secret_key = "how_to_do_anything"
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root@localhost/how_to_do_anything'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'signin'
login_manager.init_app(app)

from project1.models import User
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

from project1 import routes

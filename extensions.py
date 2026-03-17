from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
cache = Cache()
csrf = CSRFProtect()
toolbar = DebugToolbarExtension()

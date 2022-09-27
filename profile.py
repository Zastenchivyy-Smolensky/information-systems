from flask import *
from flask_login import UserMixin,LoginManager,login_required, current_user

profile = Blueprint("profile", __name__)


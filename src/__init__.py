from flask import Flask
from .config import app_config
from .views.UserView import user_api
from .views.ProfileView import profile_api
from .views import jwt
from .models import db

def create_app(env_name):
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    app.register_blueprint(user_api)
    app.register_blueprint(profile_api)

    db.init_app(app)
    jwt.init_app(app)

    return app
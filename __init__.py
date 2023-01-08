from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = "./static/uploaded"


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "app froze".encode("utf8")
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.debug = True

    db.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = "auth.dashboard"
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(userId):
        return User.query.get(int(userId))

    return app

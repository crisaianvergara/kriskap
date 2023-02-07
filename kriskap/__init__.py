from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from kriskap.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.app_context().push()
    db.init_app(app)
    login_manager.init_app(app)

    from kriskap.main.routes import main
    from kriskap.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app

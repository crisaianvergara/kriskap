from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from kriskap.config import Config
from flask_mail import Mail

db = SQLAlchemy()

# Flask Login Stuff
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

mail = Mail()


def create_app():
    """Construct the core application."""

    app = Flask(__name__, static_url_path="", static_folder="static")

    app.config.from_object(Config)

    app.app_context().push()
    db.init_app(app)

    login_manager.init_app(app)
    mail.init_app(app)

    # Imports the blueprints
    from kriskap.main.routes import main
    from kriskap.users.routes import users
    from kriskap.products.routes import products
    from kriskap.admins.routes import admins
    from kriskap.carts.routes import carts
    from kriskap.wishlist.routes import wishlists
    from kriskap.addresses.routes import addresses
    from kriskap.password.routes import password
    from kriskap.checkout.routes import checkout
    from kriskap.orders.routes import orders
    from kriskap.errors.handlers import errors

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(admins)
    app.register_blueprint(carts)
    app.register_blueprint(wishlists)
    app.register_blueprint(addresses)
    app.register_blueprint(password)
    app.register_blueprint(checkout)
    app.register_blueprint(orders)
    app.register_blueprint(errors)

    return app

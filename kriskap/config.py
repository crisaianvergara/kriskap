import os
import stripe


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

    # Postgres database and Render
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_KRISKAP")

    # SQLite database
    # SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI_KRISKAP")

    # Mail
    MAIL_SERVER = "smtp.mail.yahoo.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MY_EMAIL_SUPER")
    MAIL_PASSWORD = os.environ.get("MY_PASSWORD_YAHOO")

    # Stripe API
    STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY_KRISKAP")
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY_KRISKAP")
    stripe.api_key = STRIPE_SECRET_KEY

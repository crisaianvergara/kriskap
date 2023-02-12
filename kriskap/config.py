import os
import stripe


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI_KRISKAP")
    STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY_KRISKAP")
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY_KRISKAP")
    stripe.api_key = STRIPE_SECRET_KEY

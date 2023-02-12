from kriskap import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(250), nullable=False, default="default.png")
    password = db.Column(db.String(100), nullable=False)

    carts = relationship("Cart", back_populates="buyer")
    wishlists = relationship("Wishlist", back_populates="wisher")
    addresses = relationship("Address", back_populates="buyer")


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(250), nullable=False)

    carts = relationship("Cart", back_populates="parent_product")
    wishlists = relationship("Wishlist", back_populates="parent_product")


class Cart(db.Model):
    __tablename__ = "carts"
    id = db.Column(db.Integer, primary_key=True)

    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    buyer = relationship("User", back_populates="carts")

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    parent_product = relationship("Product", back_populates="carts")

    quantity = db.Column(db.Integer, nullable=True, default=0)


class Wishlist(db.Model):
    __tablename__ = "wishlists"
    id = db.Column(db.Integer, primary_key=True)

    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    wisher = relationship("User", back_populates="wishlists")

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    parent_product = relationship("Product", back_populates="wishlists")


class Address(db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)

    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    buyer = relationship("User", back_populates="addresses")

    house = db.Column(db.String(250), nullable=False)
    province = db.Column(db.String(250), nullable=False)
    city = db.Column(db.String(250), nullable=False)
    barangay = db.Column(db.String(250), nullable=False)

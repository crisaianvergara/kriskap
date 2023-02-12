from flask import Blueprint, render_template
from kriskap.models import Product

main = Blueprint("main", __name__)


@main.route("/home")
@main.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", products=products)
